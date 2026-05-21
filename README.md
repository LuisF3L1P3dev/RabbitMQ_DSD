# RabbitMQ_DSD

Um projeto educacional demonstrando padrões de **Produtor-Consumidor** com **RabbitMQ** em Python. Este repositório contém exemplos de como implementar sistemas de fila de mensagens usando RabbitMQ como broker.

## 📋 Descrição do Projeto

Este projeto explora conceitos de sistemas distribuídos através da implementação de:
- **Produtor (Sender)**: Envia tarefas para uma fila
- **Consumidor (Receiver)**: Processa mensagens da fila
- **Padrões de tratamento de erros**: Retry, falha, e logging
- **Persistência de mensagens**: Garantia de entrega

## 🏗️ Arquitetura

```
┌──────────┐         ┌─────────────┐         ┌──────────┐
│ Produtor │ ------> │  RabbitMQ   │ ------> │ Consumidor│
│          │         │  (Broker)   │         │          │
└──────────┘         └─────────────┘         └──────────┘
```

## 📁 Estrutura de Arquivos

### `produtor.py`
Envia 5 tarefas para a fila "tarefas" com persistência:
- Conecta ao RabbitMQ local
- Declara fila durável
- Publica mensagens com `delivery_mode=Persistent`
- Fecha conexão após enviar

### `consumidor.py`
Consumidor básico que processa mensagens:
- Conecta ao broker RabbitMQ
- Consome mensagens da fila "tarefas"
- Auto-acknowledge (reconhecimento automático)
- Loop contínuo de consumo até interrupção (CTRL+C)

### `consumidor_alo.py`
Consumidor com tratamento de erros e retry:
- Simula falha em mensagens pares
- Implementa `basic_nack()` com `requeue=True`
- Recoloca mensagens na fila para retry
- Reconhecimento manual (`auto_ack=False`)

### `consumidor_amo.py`
Consumidor com logging robusto:
- Logging estruturado com `logging` module
- Captura de erros em arquivo (`consumer_errors.log`)
- Traceback completo para debug
- Rejeição sem requeue (`requeue=False`) para evitar loops infinitos
- Tratamento elegante de interrupção

## 🚀 Como Executar

### Pré-requisitos

1. **Instalar RabbitMQ** (se não tiver):
   ```bash
   # No macOS
   brew install rabbitmq
   brew services start rabbitmq-server
   
   # No Ubuntu/Debian
   sudo apt-get install rabbitmq-server
   sudo systemctl start rabbitmq-server
   
   # No Docker
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```

2. **Instalar dependências Python**:
   ```bash
   pip install pika
   ```

### Executar o Projeto

**Terminal 1 - Iniciar o Consumidor**:
```bash
python consumidor.py
# ou com tratamento de erros
python consumidor_alo.py
# ou com logging avançado
python consumidor_amo.py
```

**Terminal 2 - Enviar Tarefas**:
```bash
python produtor.py
```

Você verá no Terminal 1:
```
Aguardando mensagens. Pressione CTRL+C Para sair
Recebido: Tarefa 0
Recebido: Tarefa 1
Recebido: Tarefa 2
Recebido: Tarefa 3
Recebido: Tarefa 4
```

## 🔑 Conceitos Principais

### **Fila Durável** (`durable=True`)
Garante que a fila persista mesmo se o RabbitMQ reiniciar.

### **Mensagem Persistente** (`delivery_mode=Persistent`)
A mensagem é gravada em disco, não se perde em caso de falha.

### **Auto-acknowledge** (`auto_ack=True`)
Remove a mensagem da fila assim que é entregue (sem garantia de processamento).

### **Reconhecimento Manual** (`auto_ack=False`)
Remove a mensagem apenas após `basic_ack()` (garante processamento).

### **Retry com Requeue** (`requeue=True`)
Devolve a mensagem para a fila se houver erro.

### **Rejeição sem Requeue** (`requeue=False`)
Descarta a mensagem (envia para Dead Letter Queue se configurada).

## 📊 Fluxo de Processamento

```
Mensagem Recebida
     ↓
[Processar]
     ↓
  ┌─────────────┬──────────────┐
  ↓             ↓              ↓
SUCESSO      ERRO RETRY    ERRO FATAL
  ↓             ↓              ↓
 ACK      NACK + REQUEUE    NACK
  ↓             ↓              ↓
Removida    Retorna à Fila   Descartada
```

## 🛠️ Troubleshooting

| Problema | Solução |
|----------|---------|
| `ConnectionRefusedError` | Verifique se RabbitMQ está rodando |
| Mensagens não chegam | Confirme que o consumidor está ativo |
| Conexão recusada na porta 5672 | Verifique firewall ou use `docker ps` |
| Mensagens perdidas | Use `durable=True` e `delivery_mode=Persistent` |

## 📚 Referências

- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Pika Library](https://pika.readthedocs.io/)
- [Message Acknowledgments](https://www.rabbitmq.com/confirms.html)
- [Reliable Messaging](https://www.rabbitmq.com/reliability.html)

## 📝 Licença

Este projeto é de código aberto e disponível para fins educacionais.

## 👨‍💻 Autor

[LuisF3L1P3dev](https://github.com/LuisF3L1P3dev)

---

**Última atualização**: Maio de 2026
