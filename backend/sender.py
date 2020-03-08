#!/usr/bin/env python

import pika

"""
RabbitMq Sender
"""


class Sender:

    def __init__(self, queue):
        self.routing_key = queue
        self.queue = queue

        self.credentials = pika.PlainCredentials('user', 'bitnami')
        self.parameters = pika.ConnectionParameters('rabbitmq',
                                                    5672,
                                                    '/',
                                                    self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def sendtoRabbitMq(self, object):
        self.channel.queue_declare(queue=self.queue)

        self.channel.basic_publish(
            exchange='', routing_key=self.routing_key, body=str(object))
        print(" [x] Data has been Sent RabbitMq")
        self.connection.close()
        
