import requests
import json

import pandas as pd

#~~~~~~~~~~~~~~~~~~~~~~~~~~~> Informações de cada player de cada guild do servidor

def atualizar_guilds():

    # pega o link da primeira pagina da api
    response_API = requests.get('https://api.tibiadata.com//v3/guilds/Collabra')

    #verificar o código de status da API
    #print(response_API.status_code)

    #converte dados da API em texto e pega somente o que tem dentro da tag highscores, highscore_list
    data = response_API.text
    parse_json = json.loads(data)
    dados = parse_json['guilds']['active']

    #cria o dataframe e apaga as colunas que não vou utilizar
    df_guild = pd.DataFrame(dados, columns=['name', 'logo_url', 'description'])
    df_guild.drop(['logo_url', 'description'], inplace=True, axis=1)

    #crio dataframe em braco pra pasar os dados da loop
    df_guild2 = pd.DataFrame(columns=['name', 'title', 'rank', 'vocation', 'level', 'joined', 'status', 'guild'])

    for i in range(len(df_guild)):
        nome_guild = df_guild.iloc[i, 0]

        # pega o link da primeira pagina da api
        response_API = requests.get('https://api.tibiadata.com//v3/guild/' + nome_guild)

        # converte dados da API em texto e pega somente o que tem dentro da tag highscores, highscore_list
        data = response_API.text
        parse_json = json.loads(data)
        dados = parse_json['guilds']['guild']['members']

        df_guild3 = pd.DataFrame(dados, columns=['name', 'title', 'rank', 'vocation', 'level', 'joined', 'status'])

        # concatena os dados dentro do mesmo dataframe
        df_guild2 = pd.concat([df_guild2, df_guild3])

        # o dataframe não traz o nome de cada guild, preciso trazer esse dado a partir da variável que está em nome_guild
