"""
    recebe 2 parametros strings, com horario no formato: 

    hora1='11:00'
    hora2='10:00'
    
    retorna uma string
    retorna a soma dos horarios passados, usando o exemplo acima a função retornaria 

    '21:00'
"""
def somaHorarios(hora1, hora2): 
    hora1 = str(hora1).split(":")
    minutos1 = int(hora1[1])
    hora1 = int(hora1[0]) * 60


    hora2 = str(hora2).split(":")
 
    minutos2 = int(hora2[1])
    hora2 = int(hora2[0]) * 60

    

    
    minutosR = (hora2 + minutos2 + hora1 + minutos1) % 60

    horaR = int((hora2 + minutos2 + hora1 + minutos1) / 60)

 
    resulTxt = ""

    if horaR < 10:
        resulTxt = resulTxt + "0"
    
    resulTxt = resulTxt + str(horaR) + ":"

    if minutosR < 10 :
        resulTxt = resulTxt +"0"
    
    resulTxt = resulTxt + str(minutosR)
    
    return resulTxt

"""
    recebe 2 parametros strings, com horario no formato: 

    hora1='11:00'
    hora2='10:00'
    
    retorna uma string
    retorna a diferença dos horarios passados, usando o exemplo acima a função retornaria 

    '23:00'
"""
def diferencaHorarios(hora1, hora2):

    hora1 = str(hora1).split(":")
 
    minutos1 = int(hora1[1])
    hora1 = int(hora1[0])

    hora2 = str(hora2).split(":")
 
    minutos2 = int(hora2[1])
    hora2 = int(hora2[0])


    minutosR = (hora2 * 60 + minutos2) - (hora1 * 60 + minutos1)
    
    if minutosR > 0:
        minutosR = minutosR % 60
    else:
        minutosR = (minutosR*-1) % 60
        minutosR = minutosR*-1
    horaR = int(((hora2 * 60 + minutos2) - (hora1 * 60 + minutos1)) / 60)

    
    

 
    if horaR < 0:
        horaR = horaR + 24;
    
    if (hora1 > hora2) and ((minutos1 != 0) or (minutos2 != 0)) and (minutos1 != minutos2):
        horaR = horaR - 1
        
        minutosR = minutosR + 60

        if horaR == -1:
            horaR = horaR + 24;
        
    

    if (hora1 == hora2) and (minutos1 > minutos2):
        horaR = horaR + 23
        minutosR = minutosR + 60
    


    resulTxt = " "

    if horaR < 10:
        resulTxt = "0"
    
    resulTxt = resulTxt + str(horaR) +":"
    
    if minutosR < 10:
        resulTxt = resulTxt + "0"
    
    resulTxt = resulTxt + str(minutosR)
    return resulTxt


"""
recebe 1 parametro string, com horario no formato: 

    hora='11:00'
    
    retorna um inteiro
    retorna a hora passado no parametro em minutos, usando o exemplo acima a função retornaria 

    '660'
"""
def converterMinutos(hora):
    hora = str(hora).split(":")

    minutos1 = int(hora[1])
    hora1 = int(hora[0]) * 60
    return minutos1 + hora1

import pandas as pd

adicional = ["22:00", "6:00"]
df =  pd.read_excel("CAMINHO DO ARQUIVO")
df["qt_marcacoes"] = 4

df["adicional_notuno"] = "00:00"    
df = df.rename(columns={'entrada': 'm0'})
df = df.rename(columns={'saida_a': 'm1'})
df = df.rename(columns={'entrada_a': 'm2'})
df = df.rename(columns={'saida': 'm3'})


df.loc[(pd.isnull(df.m1)) & (pd.isnull(df.m3) == False), ["m2"]] = None
df.loc[(pd.isnull(df.m2)) & (pd.isnull(df.m3) == False), ["m1"]] = df["m3"]
df.loc[(df.m1 == df.m3), ["m3"]] = None

df.loc[(pd.isnull(df.m1)), ["m1"]] = None
df.loc[(pd.isnull(df.m2)), ["m2"]] = None
df.loc[(pd.isnull(df.m3)), ["m3"]] = None

df.loc[(pd.isnull(df.m2)) & (pd.isnull(df.m3)), ["qt_marcacoes"]] = 2


for index, x in df.iterrows():
  i = 0
  while i < int(df["qt_marcacoes"][index]):
    
    soma = ["00:00","00:00"]
    if (converterMinutos(df['m' + str(i)][index]) >= converterMinutos(adicional[0])) or (converterMinutos(df['m'+str(i)][index]) <= converterMinutos(adicional[1])):
      soma[0] = df["m"+str(i)][index]
    else:
      soma[0] = adicional[0]

    if (converterMinutos(df["m"+str(i+1)][index]) >= converterMinutos(adicional[0])) or (converterMinutos(df["m"+str(i+1)][index]) <= converterMinutos(adicional[1])):
      soma[1] = df["m"+str(i+1)][index]
      
    else:
      soma[1] = adicional[1]
      
    if (converterMinutos(df["m"+str(i)][index]) <= converterMinutos(df["m"+str(i+1)][index])) and (converterMinutos(soma[0]) <= converterMinutos(soma[1])):
      df["adicional_notuno"][index] = somaHorarios(df["adicional_notuno"][index], diferencaHorarios(soma[0],soma[1]))
    
    if (converterMinutos(df["m"+str(i)][index]) >= converterMinutos(df["m"+str(i+1)][index])) and (converterMinutos(soma[0]) > converterMinutos(soma[1])):
      df["adicional_notuno"][index] = somaHorarios(df["adicional_notuno"][index], diferencaHorarios(soma[0],soma[1]))
    i = i+2

    if converterMinutos(df["adicional_notuno"][index]) > 480:
      i = 0
      df["qt_marcacoes"][index] = 4
      df["adicional_notuno"][index] = "00:00"
      df["m3"][index] = df["m1"][index]
      df["m1"][index] = adicional[1]
      df["m2"][index] = adicional[0]
df = df.rename(columns={'adicional_calculado': 'adicional_conam'})

df1 = pd.DataFrame(df.groupby(["reg","nome"])['adicional_notuno'].apply(list))
df2 = pd.DataFrame(df.groupby(["reg","nome"])['adicional_conam'].apply(list))
df1["adicional_conam"] = df2["adicional_conam"]
df = df1

for index, x in df.iterrows():
  resul = "00:00"
  resul1 = "00:00"
  for i in df["adicional_notuno"][index]:
    resul = somaHorarios(resul,i)
  
  for i in df["adicional_conam"][index]:
    resul1 = somaHorarios(resul1,i)
  df["adicional_notuno"][index] = resul
  df["adicional_conam"][index] = resul1

df["verificar"] = "errado"
df.loc[(df.adicional_notuno == df.adicional_conam), ["verificar"]] = "certo"
df.to_excel("Adicional total.xlsx")