import pika

# conexão com RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

# cria fila e declarando como uma queue duravel
channel.queue_declare(queue="tarefas", durable=True)

# envia mensagens
for i in range(5):
    mensagem = f"Tarefa {i}"
    

    channel.basic_publish(
        exchange="",
        routing_key="tarefas",
        body=mensagem,
        properties=pika.BasicProperties(      
            delivery_mode=pika.DeliveryMode.Persistent,  # Torna a mensagem persistente
        ))

    print(f"Enviado: {mensagem}")

connection.close()