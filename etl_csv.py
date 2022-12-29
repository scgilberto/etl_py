# -*- coding: utf-8 -*-
"""ETL_CSV.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MPNLZhio962TDqtxEfpVdvAYa-97cCVb

# ETL na pratica
"""

import pandas as pd
#importar imagen
from IPython.display import Image
from google.oauth2 import service_account

"""# Extração de dados"""

contratos = pd.read_csv('tabela_contratos.csv')

contratos.head()

datas = pd.read_csv('tabela_datas.csv')

datas.head()

empresas = pd.read_csv('tabela_empresas.csv')

empresas

"""# Transformação dos Dados"""

Image('https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/SQL_Joins.svg/800px-SQL_Joins.svg.png')

#Juntando os contrato com as empresas
contratos_mod = contratos.merge(empresas, left_on ='fk_empresa_contratada', right_on='id_empresa', how='left')

contratos_mod

#Retirando as colunas que não são necessárias.
contratos_mod.drop(columns=['id_empresa','fk_empresa_contratada'],inplace = True)

contratos_mod.head()

#buscando as datas de contratação
contratos_final = contratos_mod.merge(datas, left_on ='inicio_vigencia', right_on='id_data', how='left')

contratos_final.head()

#apagando as colunas que não serã necessarias
contratos_final.drop(columns=['inicio_vigencia','id_data'], inplace=True)

contratos_final.head()

#renomeando colunas
contratos_final.rename(columns={'data':'data_inicio_vigencia'}, inplace=True)

contratos_final.head()

#Buscando o termino da vigencia com merge
contratos_final_agora_vai = contratos_final.merge(datas, left_on ='termino_vigencia', right_on='id_data', how='left')

contratos_final_agora_vai.head()

#retirando as colunas que não é necessario
contratos_final_agora_vai.drop(columns=['termino_vigencia','id_data'], inplace=True)

#renomeando colunas
contratos_final_agora_vai.rename(columns={'data':'data_termino_vigencia'}, inplace=True)

contratos_final_agora_vai.head()

"""# Analisando o dataframe

### verificando os dados nulos
"""

contratos_final_agora_vai.count()

contratos_final_agora_vai.isnull().sum()

"""# Verificando os tipos dos dados"""

contratos_final_agora_vai.dtypes

"""## Transformando data para o formato correto"""

contratos_final_agora_vai.head()

contratos_final_agora_vai.data_inicio_vigencia = pd.to_datetime(contratos_final_agora_vai.data_inicio_vigencia, 
                                                                format='%d/%m/%Y').dt.date

contratos_final_agora_vai.data_termino_vigencia = pd.to_datetime(contratos_final_agora_vai.data_termino_vigencia, 
                                                                format='%d/%m/%Y').dt.date

for i in contratos_final_agora_vai.data_termino_vigencia:
    print(i)
    print(pd.to_datetime(i))

#Corrigindo dados na data com 31/09/2017
contratos_final_agora_vai.data_termino_vigencia = contratos_final_agora_vai.data_termino_vigencia.str.replace('31/09/2017','30/09/2017')

contratos_final_agora_vai.dtypes

contratos_final_agora_vai.head()

#adicionando colunas calculadas
contratos_final_agora_vai['tempo_contrato'] = (contratos_final_agora_vai.data_termino_vigencia - contratos_final_agora_vai.data_inicio_vigencia).dt.days

contratos_final_agora_vai

#verificando se existe dados duplicados
contratos_final_agora_vai.nome_contrato.value_counts()

#fazendo slice no dataframe
contratos_final_agora_vai[contratos_final_agora_vai.nome_contrato =='004/16']

contratos_final_agora_vai.tempo_contrato.value_counts()

#modificando o dataframe para mostrar somente tempo de contrato maior que 0
contratos_final_agora_vai = contratos_final_agora_vai[contratos_final_agora_vai.tempo_contrato > 0]

contratos_final_agora_vai.tail()

contratos_final_agora_vai.reset_index(drop=True, inplace=True)

"""# Carregamento dos Dados"""

#criando o credentials
credentials = service_account.Credentials.from_service_account_file(filename='GBQ.json'
                                                   ,scopes=["https://www.googleapis.com/auth/cloud-platform"])

#enviando o dataframe para o GBQ
contratos_final_agora_vai.to_gbq(credentials =credentials, destination_table ='curso_etl.etl_csv', if_exists='replace',
                                table_schema=[{'name':'data_inicio_vigencia', 'type':'DATE'},
                                              {'name':'data_termino_vigencia', 'type':'DATE'}])

