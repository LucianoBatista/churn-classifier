---
title: Análise Exploratória de Dados
author: Luciano
---

Antes de iniciar, vamos deixar claro o que um churn aqui nesse desafio.

>Churn é todo cliente que deixa de comprar na Magalu após um certo período de tempo.

# Análise Exploratória de Dados

Aqui iremos iniciar nossa análise pelo dataset de treino, que possui algumas informações básicas dos clientes. Mas, antes disso, como estamos falando de um problema de classificação, vale a pena entender o quanto os dados estão desbalanceados.

## Quanto nosso dado está desbalanceado?

>Lembrando que o código completo e os notebooks das EDAs podem ser encontrados no [repositório](https://github.com/LucianoBatista/churn-classifier).

```python
# is_churn proportion
df = client_tr["is_churn"].value_counts(normalize=True).reset_index()

_ = sns.countplot(x="is_churn", data=client_tr)
plt.show()
```

- IMG_CLASSES

Aqui temos um dados que está um pouco desbalanceado, sendo cerca de 82% de não ocorrência de churn, contra 18% que efetivamente deram churn.

## Como as idades estão distribuídas?

Nesse ponto, achei mais útil converter a variável de data de nascimento (`birthdate`) em idade. Após fazer essa conversão, foi possível observar como a variável está se comportando em relação ao nosso target.

```python
# convertendo em idade
client_tr["age"] = datetime.date.today().year - client_tr["birthdate"].dt.year

# plotting
_ = sns.ecdfplot(x="age", data=client_tr, hue="is_churn")
plt.show()
```

- IMG_AGE_CHURN

Pelas distribuições, vemos que existe uma maior proporção de churn em pessoas com idades mais avançadas.

## Como o Gênero Sexual (`gender`) se comporta em relação ao target?

```python
_ = sns.countplot(x="gender", data=client_tr, hue="is_churn")

```

Aparentemente, pessoas de ambos os gêneros possuem uma distribuição semelhante a do próprio target. Como menor proporção de churn.

## Onde está localizado a maior quantidade de clientes da Magalu?

Nós temos, em todos os datasets, duas variáveis de Estado:

- `state`: local onde o cliente reside.
- `delivery_state`: local de destino da entrega do pedido.

```python
# figure configuration
fig_size = (14, 6)
fig, ax = plt.subplots(figsize=fig_size)

# data
df = client_tr["state"].value_counts().reset_index()

# plotting
_ = sns.barplot(x="index", y="state", data=df_v2.sort_values(["state"]))
plt.show()
```

- IMG_STATE_DIST

Nesse primeiro momento, estaremos olhando apenas para `state`. E, conseguimos ver que existe uma grande concentração de clientes no **Estado st15**, muito mais que nos seguintes Estados. 

Veja também que a distribuição é praticamente idêntica para *Churn* e *não Churn*.

