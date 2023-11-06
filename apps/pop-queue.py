import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.identity.aio import DefaultAzureCredential

import sys, os

QUEUE_NAME = "test"
connection = os.getenv('CONNECTION_STRING')
credential = DefaultAzureCredential()

async def run():
    # create a Service Bus client using the connection string
    async with ServiceBusClient.from_connection_string(
        conn_str=connection,
        logging_enable=True) as servicebus_client:
        async with servicebus_client:
            # get the Queue Receiver object for the queue
            receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME)
            async with receiver:
                while True:
                    received_msgs = await receiver.receive_messages(max_wait_time=5, max_message_count=20)
                    for msg in received_msgs:
                        print("Received: " + str(msg))
                        # complete the message so that the message is removed from the queue
                        await receiver.complete_message(msg)
                        sys.exit()


asyncio.run(run())
