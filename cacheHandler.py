import pandas as pd
#Questo documento agisce come database per le informazioni necessarie al servizio

#Crea una variabile dataframe(database) con le informazioni lette dal documento csv
main_df = pd.read_csv("cache_msg_df.csv", usecols=['date', 'dest', 'content'])

def UpdateDataFrame():
    #Aggiorna la variabile nel caso di modifiche
    main_df = pd.read_csv("cache_msg_df.csv", usecols=['date', 'dest', 'content'])


def RegisterMsg(date, dest, content):
    
    new_df = pd.DataFrame(data={
        'date':[date],
        'dest':[dest],
        'content': [content]
    })
    pd.concat([main_df, new_df]).to_csv('cache_msg_df.csv', sep=",", encoding='utf-8')
    UpdateDataFrame()
    return 1

def FindMsgContent(date):
    for user in main_df['date']:
        if user == date:
            print("Utente trovato")
            #Dopo aver trovato la riga corrispondente al nomeutente indicato
            #ritorno l'indirzzo ip ad esso associato e lo faccio ritornare alla funzione
            content = main_df.iloc[main_df.index[(main_df['date'] == date)]]['content']
            return content.values[0]
    print("Utente non trovato")
    return 0

def Login(date, dest, content):
    #Verifico se la coppia date-dest esiste nel dataframe
    if (((main_df['date'] == date) & (main_df['dest'] == dest)).any()):
        print("Autenticazione completata")
        #A login effettuato aggiorno l'ip dell'utente e la salvo nel csv
        main_df.at[(main_df['date'] == date), ['content']] = content
        main_df.to_csv('cache_msg_df.csv', sep=",", encoding='utf-8', index=False)
        UpdateDataFrame()
        return 1
    else:
        print("dest errata o nome utente inesistente")
        return 0