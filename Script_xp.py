import requests
import json

import pandas as pd

#~~~~~~~~~~~~~~~~~~~~~~~~~~~> Informações de XP de cada jogador do servidor

def atualizar_xp():

  #pega o link da primeira pagina da api
  response_API = requests.get('https://api.tibiadata.com/v3/highscores/Collabra/experience/all/1')

  #verificar o código de status da API
  #print(response_API.status_code)

  #converte dados da API em texto e pega somente o que tem dentro da tag highscores, highscore_list
  data = response_API.text
  parse_json = json.loads(data)
  dados = parse_json['highscores']['highscore_list']

  #cria df_xp e salva primeira lista importada
  df_xp = pd.DataFrame (dados, columns = ['rank', 'name', 'vocation', 'world', 'level', 'value'])

  #inicia for loop pra baixar os dados das demais paginas
  for i in range(2,20):
    response_API = requests.get('https://api.tibiadata.com/v3/highscores/Collabra/experience/all/' + str(i))
    data = response_API.text
    parse_json = json.loads(data)
    dados = parse_json['highscores']['highscore_list']
    df_xp2 = pd.DataFrame (dados, columns = ['rank', 'name', 'vocation', 'world', 'level', 'value'])

    #concatena os dados dentro do mesmo dataframe
    df_xp = pd.concat([df_xp,df_xp2])

  df_xp = df_xp.reset_index()
  df_xp.drop('index', inplace=True, axis=1)

  #cria coluna com a data de hoje
  df_xp['date'] = pd.to_datetime('today')

  #cria linha vazia ao final do df_xp para não bugar qd concatenar os dados
  #df_xp_vazio = pd.Series([None, None, None, None, None, None, None], index=['rank', 'name', 'vocation', 'world', 'level', 'value', 'date'])

  #df_xp = df_xp.append(df_xp_vazio, ignore_index=True)

  #cria csv com os dados iniciais
  #df_xp.to_csv('C:/Users/Mateus/PycharmProjects/Tibia dados/xp.csv')

  #adiciona dados ao csv do dia anterior
  df_xp.to_csv('C:/Users/Mateus/PycharmProjects/Tibia dados/xp.csv', mode='a', index=True, header=False, line_terminator='\n')