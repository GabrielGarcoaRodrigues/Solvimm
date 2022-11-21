#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importando as bibliotecas necessárias
import pandas as pd
import numpy as np


# In[2]:


#importando o priemiro database
df = pd.read_csv('movies.csv', sep=';')
#importando o segundo database
df2 = pd.read_csv('customers_rating.csv', sep=';')


# In[3]:


#checando se tem algum valor nulo
df.isnull().values.any()
df2.isnull().values.any()


# In[4]:


#Separar o 'Nome' do 'Ano' do filme
df[['Nome', 'Ano']] = df['Nome_Ano'].str.split(', ', expand=True)
df


# In[5]:


#Eliminando a coluna Nome_Ano
df.drop('Nome_Ano', axis=1, inplace=True)

#Removendo os parenteses dos nomes e dos anos
df['Nome'] = df['Nome'].str.strip('(')
df['Ano'] = df['Ano'].str.strip(')')

df


# In[6]:


#1.1 Quantos filmes estão disponíveis no dataset?
print('O dataset tem {0} filmes!'.format(df.shape[0]))


# In[7]:


#1.2. Qual é o nome dos 5 filmes com melhor média de avaliação?
mean = df2.groupby('Movie_Id').mean()
mean = mean.sort_values('Rating', ascending=False).head(5)['Rating']
ids = pd.DataFrame(mean).reset_index()
best_ids = ids['Movie_Id'].to_list()
df.query('ID == @best_ids')['Nome'].to_list()


# In[8]:


#1.3 Os 9 anos com menos lançamentos de filmes
df['Ano'] = df['Ano'].astype(int)
count_year = df.groupby(['Ano']).size().nsmallest(9)
worse = pd.DataFrame(count_year).reset_index()
worse.rename(columns={0: 'Lançamentos'}, inplace = True)
print("Os 9 anos com menos lançamentos de filmes são:\n")
worse


# In[9]:


#1.4. Quantos filmes que possuem avaliação maior ou igual a 4.7, considerando apenas os filmes avaliados na última data de avaliação do dataset?
last_date = df2['Date'].max()
order_rating = df2[(df2['Date'] == last_date)]
order_rating = order_rating.groupby('Movie_Id').mean()
order_rating = order_rating.sort_values('Rating', ascending=False)['Rating']
order_rating = order_rating.reset_index()
movies = order_rating[order_rating['Rating']>=4.7]
print('{0} filmes!'.format(movies.shape[0]))


# In[10]:


#1.5. Dos filmes encontrados na questão anterior, quais são os 10 filmes com as piores notas e quais as notas?
list = (movies.iloc[-10:])
last = list['Movie_Id'].to_list()
data = df.query('ID == @last')['Nome'].reset_index()
nova = list['Rating'].to_list()
data.insert(2, "rating", nova)
data = data.drop(['index'], axis=1)
data


# In[11]:


#1.6 Quais os id's dos 5 customer que mais avaliaram filmes e quantas avaliações cada um fez?
count_cust = df2.groupby(['Cust_Id']).size().nlargest(5)
top_cust = pd.DataFrame(count_cust).reset_index()
top_cust.rename(columns={0: 'Avaliações'}, inplace = True)
print("O ID dos 5 Customers que mais avaliaram filmes e quantas vezes eles avaliaram:")
top_cust

