import pika

# conexão com RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

# cria fila
channel.queue_declare(queue="tarefas")

# envia mensagens
for i in range(5):
    mensagem = f"Tarefa {i}"
    
    channel.basic_publish(
        exchange="",
        routing_key="tarefas",
        body=mensagem
    )

    print(f"Enviado: {mensagem}")

connection.close()