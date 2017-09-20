#!/usr/bin/env python

import sys
import base64
import cv2
import json
import numpy as np
import os

import pyspark
from pyspark import streaming
from pyspark.streaming import kafka


def process_frame(dataset, face_cascade):
    base_path = os.path.dirname(os.path.realpath(__file__))
    cascade_path = os.path.join(
        base_path, 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(cascade_path)

    data = dataset.collect()
    for datum in data:
        try:
            jpg = base64.b64decode(datum.get('data', None))
        except TypeError:
            return
        frame = cv2.imdecode(np.fromstring(
            jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        datum['data'] = base64.b64encode(frame)
#        producer.send(OUT_TOPIC_NAME,
#                      key=datum['camera_id'],
#                      value=json.dumps(datum))


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "noop":
        return
    if len(sys.argv) != 8:
        print "Usage: spark_stream_analytics.py <spark_master> <zk_quorum> <topic_name> <batch_duration> <save_to>"
        print "Example: spark_stream_analytics.py local[4] zk-kafka-1-0.zk-kafka-1:2181,zk-kafka-1-1.zk-kafka-1:2181,zk-kafka-1-2.zk-kafka-1:2181 video-stream 5 hdfs://hdfs-namenode:8020/demo"
        print "<spark_master> - spark master to use: local[4] or spark://HOST:PORT"
        print "<zk_quorum> - zk quorum to connect: zk-kafka-1-0.zk-kafka-1:2181,zk-kafka-1-1.zk-kafka-1:2181,zk-kafka-1-2.zk-kafka-1:2181"
        print "<topic_name> - kafka topic name: twitter-stream"
        print "<batch_duration> - spark streaming batch duration ~ how often data will be written"
        exit(-1)

    spark_master = sys.argv[1]
    zk_quorum = sys.argv[2]
    topic_name = sys.argv[3]
    batch_duration = int(sys.argv[4])

    sc = pyspark.SparkContext(spark_master, appName="VideoTics")
    ssc = streaming.StreamingContext(sc, batch_duration)

    video = kafka.KafkaUtils.createStream(
        ssc, zk_quorum, "video-consumer", {topic_name: 1}).map(lambda x: json.loads(x[1]))

    output = video.foreachRDD(process_frame)
    output.pprint()

    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__":
    main()
