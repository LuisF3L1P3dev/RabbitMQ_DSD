import pika
import sys
import os
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.queue_declare(queue='tarefas', durable=True)

def main():

    def callback(ch, method, properties, body):

        mensagem = body.decode()

        try:
            print(f"[x] Processando: {mensagem}")
            numero = int(mensagem.split()[-1])
            time.sleep(2)
            print(f"n: {numero}")

            # falha simulada nas mensagens pares
            if numero % 2 == 0:
                raise Exception("Erro simulado!")

            print(f"[✓] Sucesso: {mensagem}")


            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f"[!] Falha: {mensagem}")
            print(e)

            # devolve mensagem para fila
            ch.basic_nack( delivery_tag=method.delivery_tag, requeue=True)

    channel.basic_consume(queue='tarefas', on_message_callback=callback, auto_ack=False)

    print('Aguardando mensagens...')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrompido')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)