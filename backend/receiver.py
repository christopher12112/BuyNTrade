#!/usr/bin/env python

import pika
import db
import json

"""
RabbitMq Receiver
"""
class Receiver:

    def __init__(self, queue):

        self.queue = queue
        self.credentials = pika.PlainCredentials('user', 'bitnami')
        self.parameters = pika.ConnectionParameters('rabbitmq',
                                                    5672,
                                                    '/',
                                                    self.credentials)

        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=self.queue)

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)

    def startReceiving(self):
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')

        self.channel.start_consuming()
        self.channel.close()

    def getMessages(self):
        # Get ten messages and break out
        for method_frame, properties, body in self.channel.consume(self.queue):

            # Display the message parts
            # print(method_frame)
            # print(properties)

            # Acknowledge the message
            self.channel.basic_ack(method_frame.delivery_tag)

            # Escape out of the loop after 10 messages
            if method_frame.delivery_tag == 1:
                break

        # Cancel the consumer and return any pending messages
        requeued_messages = self.channel.cancel()
        print('Requeued %i messages' % requeued_messages)

        response = False
        if self.queue == 'login':
            d = db.Db()
            body = body.decode('utf-8')
            body = body.replace("\'", "\"")
            res = json.loads(body)
            username = res['username']
            password = res['password']
            r = d.do_login(username, password)

            if r == False:
                response = False

            response = r
        elif self.queue == 'registration':
            d = db.Db()
            body = body.decode('utf-8')
            body = body.replace("\'", "\"")
            res = json.loads(body)
            UserName = res['UserName']
            Email = res['Email']
            Password = res['Password']
            Address = res['Address']
            ContactNo = res['ContactNo']
            r = d.do_registration({'UserName': UserName, 'Email': Email,
                                   'Password': Password, 'Address': Address, 'ContactNo': ContactNo})

            if r == False:
                response = False

            response = r
        else:
            response = False
        # Close the channel and the connection
        self.channel.basic_qos(prefetch_count=1)
        self.channel.close()
        self.connection.close()
        return response
