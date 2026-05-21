Aqui está o documento totalmente organizado em **Markdown**. Apliquei uma formatação limpa e profissional, utilizando cabeçalhos lógicos, blocos de código para comandos, listas estruturadas para os requisitos e caixas de destaque para pontos que exigem atenção extra.

Você pode copiar o conteúdo abaixo diretamente para o seu editor de Markdown ou Notion:

---

# Atividade Prática: Mensageria com RabbitMQ

**Disciplina:** Sistemas Distribuídos

**Discente:** [Insira seu nome aqui]

---

## 🎯 Objetivo

Implementar um sistema de mensageria utilizando RabbitMQ, compreendendo na prática o funcionamento de filas, durabilidade de mensagens e as semânticas de entrega *at-least-once* e *at-most-once*.

## 📖 Contexto

Em sistemas distribuídos, o desacoplamento entre produtores e consumidores de mensagens é um padrão fundamental. O RabbitMQ é um *message broker* que implementa o protocolo AMQP e permite que mensagens sejam enfileiradas e entregues de forma confiável, mesmo quando os consumidores estão temporariamente indisponíveis.

Nesta atividade, você irá simular cenários reais de produção e consumo de mensagens, variando o comportamento do consumidor (online/offline) e a semântica de entrega.

---

## 🛠️ Pré-requisitos

* **RabbitMQ** instalado localmente ou via Docker:
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

```


* **Python 3** com a biblioteca `pika` instalada:
```bash
pip install pika

```


* **Interface de Gerenciamento:** Acessível em [http://localhost:15672](https://www.google.com/search?q=http://localhost:15672) (Credenciais: `guest` / `guest`)

---

## 📝 Questões da Atividade

### Questão 1 – Fila Durável e Consumidor Offline

Implemente dois scripts Python: `produtor.py` e `consumidor.py`. O produtor deve publicar 5 mensagens em uma fila chamada `tarefas`. A fila deve ser configurada como durável e as mensagens devem ser marcadas como persistentes, garantindo que sobrevivam a uma reinicialização do broker.

**Fluxo de simulação exigido:**

1. Execute o produtor com o consumidor ainda *offline*.
2. Verifique na interface de gerenciamento se as mensagens estão acumuladas na fila (coluna *Ready*).
3. Inicie o consumidor e observe o recebimento das mensagens acumuladas.
4. Execute novamente o produtor com o consumidor já *online* e observe a entrega em tempo real.

> 📦 **Entregáveis da Q1:** Código-fonte dos dois scripts + capturas de tela demonstrando:
> * **(a)** A fila com mensagens aguardando (com o consumidor offline).
> * **(b)** O consumidor recebendo as mensagens acumuladas logo após iniciar.
> 
> 

---

### Questão 2 – Semântica *At-Least-Once* (Pelo menos uma vez)

Modifique o consumidor da Questão 1 para implementar a semântica *at-least-once*. Nesta abordagem, o ACK (confirmação) só é enviado ao broker após o processamento bem-sucedido da mensagem. Para simular uma falha, lance uma exceção nas mensagens de índice par e observe o broker reenviar a mensagem.

Salvar o arquivo como: `consumidor_alo.py`.

📌 **Pontos de Atenção:**

* Use `auto_ack=False` ao registrar o consumo.
* **Em caso de erro:** Use `channel.basic_nack(requeue=True)` para recolocar a mensagem na fila.
* **Em caso de sucesso:** Use `channel.basic_ack()` para confirmar o processamento.

> 📦 **Entregáveis da Q2:** Código-fonte + capturas de tela mostrando a mensagem sendo reenviada pelo broker após a falha simulada e, em seguida, sendo processada com sucesso.

---

### Questão 3 – Semântica *At-Most-Once* (No máximo uma vez)

Implemente a variante *at-most-once*. Nesta abordagem, o ACK é enviado automaticamente pelo broker no exato momento em que a mensagem é entregue ao consumidor, antes mesmo do processamento. Se o consumidor falhar durante o processamento, a mensagem é perdida permanentemente. Demonstre isso simulando uma falha após o recebimento.

Salvar o arquivo como: `consumidor_amo.py`.

📌 **Pontos de Atenção:**

* Use `auto_ack=True` ao registrar o consumo.
* Introduza uma exceção no *callback* para simular uma falha de processamento logo após a entrega.
* Verifique na interface do RabbitMQ que a mensagem foi removida da fila, mesmo sem ter sido processada com sucesso.

> 📦 **Entregáveis da Q3:** Código-fonte + capturas de tela mostrando a fila zerada após a entrega e o log de erro detalhado no terminal do consumidor.

---

### Questão 4 – Análise Comparativa

Com base na sua implementação prática, responda de forma dissertativa:

1. Em que tipos de sistemas cada semântica (*at-least-once* e *at-most-once*) é mais apropriada?
2. Cite ao menos um exemplo de sistema do mundo real para cada uma delas.
3. Justifique suas escolhas considerando o impacto de aceitar a **duplicação de mensagens** versus aceitar a **perda de mensagens**.

---

## 📭 Orientações de Entrega

* **Formato do Arquivo:** Submeta um arquivo compactado (`.zip`) contendo todos os scripts Python criados e um relatório final em formato PDF ou DOCX.
* **Conteúdo do Relatório:** O documento deve conter as capturas de tela solicitadas em cada questão, acompanhadas de uma breve legenda explicando o comportamento demonstrado.
* **Evidências Visuais:** As capturas devem exibir claramente o terminal do produtor/consumidor e, nos momentos indicados, o painel da interface de gerenciamento do RabbitMQ.

> 🛑 **Aviso sobre Plágio:** O código deve ser estritamente original. Implementações idênticas ou suspeitas de plágio entre alunos implicarão na anulação imediata da atividade para todos os envolvidos.