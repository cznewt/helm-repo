#!/usr/bin/env python

import json
import sys

import click
import kafka as kafka_client


def process_comma_separated_option(option):
    return option.split(',') if option else None


@click.command()
@click.option('--kafka', default=None,
              help="A comma-separated list of Kafka bootstap servers")
@click.option('--topic', default="twitter-stream",
              help="Kafka topic where the video streams will be published")
@click.option('--hdfs', default=None,
              help="A comma-separated list of HDFS-namenode servers")
@click.option('--path', help="Path in HDFS to save Tweets")
def _main(kafka, topic, hdfs, path):
    if kafka:
        click.echo("Kafka bootstrap servers: %s" % kafka)
        producer = kafka_client.KafkaProducer(bootstrap_servers=kafka,
                                            value_serializer=str.encode)
    else:
        click.echo("HDFS server: %s" % hdfs)
        from pyhdfs import HdfsClient
        client = HdfsClient(hosts=hdfs, user_name='root')


def main():
    _main(auto_envvar_prefix='VIDEOPUB')


if __name__ == '__main__':
    main()
