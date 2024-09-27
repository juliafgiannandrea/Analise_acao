#Importar bibliotecas:
import requests
import re 
import numpy as np
import pandas as pd

#Permitir acesso
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4ODI3MTQ0LCJqdGkiOiI0MDNmMzhiNjZkYmM0YjcyYmQ5YTY1NzI5NWM0NzQ5MSIsInVzZXJfaWQiOjM5fQ.s4O9vn_fDum7yMmGVcFUZcgMCe29dJWUsbHAhzA-tGM"
headers = {'Authorization': 'JWT {}'.format(token)}

#Planilhão: 
params = {'data_base': '2023-04-03'}  

    #pegar a API:
planilhao = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
planilhao = planilhao.json()
planilhao = planilhao["dados"]

    #criar dataframe com os dados do planilhão 
dfplanilhao = pd.DataFrame(planilhao) 

    #colunas de interesse
col_planilhao = ["ticker", "data_base", "roe", "volume"]
df_planilhao = dfplanilhao[col_planilhao]

    #ações com os 15 maiores roe (selecionei 15 pq vem algumas repetidas):
df_top = df_planilhao.nlargest(15,'roe')

    #Eliminar pelo maior volume: 
        #cria nova coluna que tem apenas as 4 letras iniciais de cada ação para conseguir filtrar e eliminar as ações repetidas: 
df_top['base_ticker'] = df_top['ticker'].str[:4]

    #Identifica o índice do maior volume para cada grupo de 'base_ticker'
idx = df_top.groupby('base_ticker')['volume'].idxmax()
        #dentro de cada grupo, busca o index da linha que tem o maior valor na coluna 'volume'
        #groupby: agrupa dados num df com base em uma mais colunas (divide os dados em grupos - encontra valor máximo em cada grupo: idmax - combina os resultados num novo objeto)

    #Filtra o DataFrame para manter apenas as linhas com os maiores volumes (que foram as encontradas pelo idx)
df_top10 = df_top.loc[idx].reset_index(drop=True)



#Preço corrigido: para cada uma das ações no df df_top10 - 10 maiores roe

dataframes = []

for acao in df_top10["ticker"]:
    params1 = {'ticker': acao, 'data_ini': '2023-04-01', 'data_fim': '2024-04-01'}
    preco = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido',params=params1, headers=headers)
    preco = preco.json()
    preco = preco["dados"]
    df_preco = pd.DataFrame(preco)
    col_preco = ["ticker", "data", "abertura","fechamento"]
    df_preco= df_preco[col_preco]
    df_preco = pd.DataFrame(df_preco) 

    #manipular os dados do data frame:
        #pegar o valor de abertura na data inicial do período: 
    abertura = df_preco.iloc[-0,-1] 

        #pegar o valor de fechamento na data final do período:
    fechamento = df_preco.iloc[-1,-1] 

        #calculo do retorno (é o que usarei para comparar com a IBOVESPA)
    retorno = ((fechamento - abertura)/ abertura)*100

        #adiciona no df a coluna retorno
    df_preco["retorno"] = retorno 

        #pega só a ultima linha 
    df_preco = df_preco.iloc[[-1]]

        #Colunas de interesse do df
    quero = ["ticker", "retorno"]
    df_preco = df_preco[quero]

        #adicionar numa lista vazia cada df das ações analisadas
    dataframes.append(df_preco) 

        #df com os tickers do top 10 roe e seus respectivos retornos
df_final = pd.concat(dataframes,ignore_index=True)


############################################################################################################


    #Calcular o rendimento total da carteira de ações do top10 roe
df_carteira_roe = df_final.copy()
        #no rendimento da carteira: cada ação representa 10%: multiplicar por 0.1
df_carteira_roe["retorno"] = df_carteira_roe["retorno"]* 0.1 
soma_total = df_carteira_roe['retorno'].sum()  
        #formatar para sair em porcentagem:
retorno_formatado_roe = f"{soma_total:.2f}%"  #retorno da carteira de ações do top10 roe


###########################################################################################################

#Calcular o IBOVESPA do período:

params_ibov = {
'ticker': 'ibov',
'data_ini': '2023-04-01',
'data_fim': '2024-04-01'
}

#pegar API:
ibovespa = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params_ibov, headers=headers)
response_ibov = ibovespa.json()
dados_ibov  = response_ibov['dados']  

df_ibov = pd.DataFrame(dados_ibov)
ibov_abertura = df_ibov.iloc[0,-1]
ibov_fechamento = df_ibov.iloc[-1,-1]
retorno_ibov = ((ibov_fechamento - ibov_abertura)/ibov_abertura)*100 
df_final["Ibovespa"] = retorno_ibov

#Comparar com o ibovespa: 
df_final["resultado"] = np.where(
    df_final["retorno"] > df_final["Ibovespa"], "ganha",
    np.where( df_final['retorno'] < df_final["Ibovespa"], "perde", "empata")
    )


##############################################################################################################


#Magic Formula: 

col = ["ticker", "roic", "earning_yield", 'volume' ] #do planilhao eu pego essas colunas 
df_comparacao = dfplanilhao[col]


    #Ranking das ações (earning yield e roic): crio novas colunas no data frame com os respectivos rankings
        #pego 35 pq vem ações repetidas 
    #top 35 roic: 
df_top35_roic = df_comparacao.nlargest(35,"roic").reset_index(drop = True)
df_top35_roic.index = range(1, len(df_top35_roic) + 1)
df_top35_roic["index_roic"] = df_top35_roic.index #nova coluna com o ranking do roic 

    #top 35 ey:
df_top35_ey = df_comparacao.nlargest(35,"earning_yield").reset_index(drop = True) 
df_top35_ey.index = range(1, len(df_top35_ey) + 1)
df_top35_ey["index_ey"] = df_top35_ey.index #nova coluna com o ranking do ey 

    #juntar numa data frame o ranking (do ey e do roic), o nome e o volume das ações: 
df_merged  = pd.merge(df_top35_ey[["ticker", "index_ey", "volume"]], 
                      df_top35_roic[["ticker", "index_roic"]], 
                      on = "ticker", 
                      how = "inner")

    #ranking médio: (soma das posições/do ranking)
df_merged["media"] = df_merged["index_ey"] + df_merged["index_roic"]
df_sorted = df_merged.sort_values(by=['media'], ascending=[True])
df_sorted = df_sorted.reset_index(drop = True)

    #para eliminar as repetidas (filtrar pelo maior volume):
df_merged['ticker_base'] = df_merged['ticker'].str[:4] #identificar as ações repetidas
id =df_merged.groupby('ticker_base')['volume'].idxmax() #maior volume
df_final_sorted = df_merged.loc[id].reset_index(drop=True)

df_final_sorted = df_final_sorted.sort_values(by="media", ascending=True).reset_index(drop=True)
df_final_sorted = df_final_sorted.nsmallest(10,"media") #só os top10 nos dois rankings 


##################################################################################################################

# Comparação das ações do Magic Formula com o Ibovespa:

df_ibov_magic = []
for acao in df_final_sorted["ticker"]:
    params2 = {'ticker': acao, 'data_ini': '2023-04-01', 'data_fim': '2024-04-01'}
    preco = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido',params=params2, headers=headers)
    preco = preco.json()
    preco = preco["dados"]
    df_preco = pd.DataFrame(preco)
    col_preco = ["ticker", "data", "abertura","fechamento"]
    df_preco= df_preco[col_preco]
    df_preco = pd.DataFrame(df_preco) 

    #manipular os dados do data frame:

        #pegar o valor de abertura na data inicial do período:
    abertura = df_preco.iloc[0,-2]
        #pegar o valor de fechamento na data final do período:
    fechamento = df_preco.iloc[-1,-1] 
        #calculo do retorno (é o que usarei para comparar com a IBOVESPA)
    retorno = ((fechamento - abertura)/ abertura)*100

       #adiciona no df a coluna retorno
    df_preco["retorno"] = retorno 
        #pega só a ultima linha
    df_preco = df_preco.iloc[[-1]] 

        #Colunas de interesse do df
    quero = ["ticker", "retorno"]
    df_preco = df_preco[quero]

        #adicionar numa lista vazia cada df (dos tickers específicos)
    df_ibov_magic.append(df_preco) 

        #df com os tickers do top 10 roe e seus respectivos retornos; ignore index para sair de 0 - 9 :
df_final_magic = pd.concat(df_ibov_magic,ignore_index=True) 

df_final_magic["Ibovespa"] = retorno_ibov

#para comparar com o ibovespa: 
df_final_magic["resultado"] = np.where(
    df_final_magic["retorno"] > df_final_magic["Ibovespa"], "ganha",
    np.where( df_final_magic['retorno'] < df_final_magic["Ibovespa"], "perde", "empata")
    )


####################################################################################################################


#Rendimento total da carteira de ações oriundas do magic formula: 

    #Calcular o rendimento total da carteira de ações 
df_carteira_magic= df_final_magic.copy()

        #no rendimento da carteira: cada ação representa 10% 
df_carteira_magic["retorno"] = df_carteira_magic["retorno"]* 0.1 
soma_total_magic = df_carteira_magic['retorno'].sum()  
        #formatar para sair em porcentagem:
retorno_formatado_magic = f"{soma_total_magic:.2f}%"  #retorno da carteira de ações do top10 magic


####################################################################################################################

# OUTPUT:

    #ROE:

print("Carteira de ações de acordo com o roe:")
print(df_final)
print("Retorno da carteira top10 roe:", retorno_formatado_roe)

    #MAGIC FORMULA

print("Carteira de ações de acordo com a Magic Formula")
print(df_final_magic)
print("Retorno da carteira top10 MagicFormula:", retorno_formatado_magic)