import pika
import sys
import os
import time

# conexão com o broker RabbitMQ local
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# fila 'tarefas' como duravel
channel.queue_declare(queue='tarefas', durable=True)

def callback(ch, method, properties, body):
    print(f"Recebido: {body.decode()}")
    time.sleep(0.5)

# configura o consumidor para a fila 'tarefas'
channel.basic_consume(queue='tarefas', on_message_callback=callback, auto_ack=True)
print('Aguardando mensagens. Pressione CTRL+C Para sair' )
channel.start_consuming()