#!/usr/bin/env python

import click
import base64
import cv2
import json
import time
import urllib
import numpy as np
import kafka as kafka_client


def process_comma_separated_option(option):
    return option.split(',') if option else None


@click.command()
@click.option('--camid', default='camera-01',
              help="Camera ID")
@click.option('--mjpg',
              help="MJPG stream URL")
@click.option('--kafka', default=None,
              help="A comma-separated list of Kafka bootstap servers")
@click.option('--topic', default="twitter-stream",
              help="Kafka topic where the video streams will be published")
def _main(camid, mjpg, kafka, topic):
    stream = urllib.urlopen(mjpg)
    bytes = ''

    while True:
        bytes += stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            frame = cv2.imdecode(np.fromstring(
                jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            payload = {
                'camera_id': camid,
                'timestamp': int(time.time()),
                'rows': frame.shape[0],
                'cols': frame.shape[1],
                'type': 'uint8',
                'data': base64.b64encode(jpg)
            }

            producer = kafka_client.KafkaProducer(
                bootstrap_servers=kafka,
                batch_size=512000,
                api_version=(0, 10, 1))

            producer.send(topic,
                          key=camid,
                          value=json.dumps(payload))


def main():
    _main(auto_envvar_prefix='VIDEOPUB')


if __name__ == '__main__':
    main()
