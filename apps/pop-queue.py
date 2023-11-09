import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.identity.aio import DefaultAzureCredential
import logging
import json
import sys, os
import weaviate_utils

logging.basicConfig(level=logging.INFO)

client = weaviate_utils.weaviate_connection()
logging.info('\nclient.isReady(): %s', client.is_ready())
logging.info('cluster.get_nodes_status(): %s', client.cluster.get_nodes_status())

class_obj = {
    "class": "Question",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "generative-openai": {
          "model": "gpt-3.5-turbo",  # Optional - Defaults to `gpt-3.5-turbo`
        }
    }
}

#
# Create the class if its not there
#

if client.schema.exists('Question'):
    logging.info("Question class already exists, skipping class creation.")
else:
    logging.info(f'\nCreating the Question class using the openai vectorizer.')
    client.schema.create_class(class_obj)
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

                        data = json.loads(str(msg))  # Load data

                        client.batch.configure(batch_size=100)  # Configure batch
                        with client.batch as batch:  # Initialize a batch process
                            for i, d in enumerate(data):  # Batch import data
                                print(f"importing question: {i+1}")
                                properties = {
                                    "answer": d["Answer"],
                                    "question": d["Question"],
                                    "category": d["Category"],
                                }
                                batch.add_data_object(
                                    data_object=properties,
                                    class_name="Question"
                                )
                        # complete the message so that the message is removed from the queue
                        await receiver.complete_message(msg)
                        sys.exit()
asyncio.run(run())
