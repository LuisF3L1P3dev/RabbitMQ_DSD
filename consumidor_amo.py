import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.queue_declare(queue='tarefas', durable=True)

def callback(ch, method, properties, body):

    mensagem = body.decode()

    print(f"[x] Recebido: {mensagem}")

    time.sleep(2)

    # falha simulada
    raise Exception("Falha após recebimento!")

channel.basic_consume(queue='tarefas', on_message_callback=callback, auto_ack=True)

print('Aguardando mensagens...')
channel.start_consuming()