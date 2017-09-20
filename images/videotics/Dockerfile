FROM mirantisworkloads/spark:2.2.0

ADD spark_stream_analytics.py /
RUN git clone https://github.com/datastax/python-driver.git && cd python-driver && python setup.py install && cd /
RUN spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.0 spark_stream_analytics.py noop
