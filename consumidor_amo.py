import pika
import time
import logging
import traceback

# logger para mensagens mínimas no terminal
logger = logging.getLogger('consumidor')
logger.setLevel(logging.INFO)
ch_logger = logging.StreamHandler()
ch_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
ch_logger.setFormatter(formatter)
logger.addHandler(ch_logger)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.queue_declare(queue='tarefas', durable=True)

def callback(ch, method, properties, body):
    try:
        mensagem = body.decode()
        logger.info(f"[x] Recebido: {mensagem}")
        time.sleep(2)

        # falha simulada
        raise Exception("Falha após recebimento!")

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        # mostra apenas uma mensagem curta no terminal
        logger.error(f"Erro ao processar mensagem: {e}")
        # grava o traceback completo em arquivo para análise posterior
        with open('consumer_errors.log', 'a', encoding='utf-8') as f:
            f.write(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            traceback.print_exc(file=f)
        # rejeita a mensagem para evitar loop (não requeue)
        try:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception:
            pass

# consome sem ack automático para só remover mensagem em caso de sucesso
channel.basic_consume(queue='tarefas', on_message_callback=callback, auto_ack=False)

logger.info('Aguardando mensagens...')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    logger.info('Interrompido pelo usuário')
finally:
    try:
        channel.stop_consuming()
    except Exception:
        pass
    connection.close()
    logger.info('Conexão fechada')