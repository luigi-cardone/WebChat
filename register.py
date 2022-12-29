import pandas as pd
#Questo documento agisce come database per le informazioni necessarie al servizio

#Crea una variabile dataframe(database) con le informazioni lette dal documento csv
main_df = pd.read_csv("register_df.csv", usecols=['Username', 'Password', 'Address'])
def UpdateDataFrame():
    #Aggiorna la variabile nel caso di modifiche
    main_df = pd.read_csv("register_df.csv", usecols=['Username', 'Password', 'Address'])


def Register(username, password):
    #verifico se il nome utente è già presente del dataframe
    for name in main_df['Username']:
        if name == username:
            print("Nome utente già esistente")
            return 0
    else:
        #Se lo username non è già esistente creo una nuova riga nel dataframe con le nuove informazioni
        new_df = pd.DataFrame(data={
            'Username':[username],
            'Password':[password],
            'Address': [""]
        })
        #Unisco la nuova riga con il dataframe esistente
        pd.concat([main_df, new_df]).to_csv('register_df.csv', sep=",", encoding='utf-8')
        UpdateDataFrame()
        return 1

def FindUserAddress(username):
    for user in main_df['Username']:
        if user == username:
            print("Utente trovato")
            #Dopo aver trovato la riga corrispondente al nomeutente indicato
            #ritorno l'indirzzo ip ad esso associato e lo faccio ritornare alla funzione
            address = main_df.iloc[main_df.index[(main_df['Username'] == username)]]['Address']
            return address.values[0]
    print("Utente non trovato")
    return 0

def Login(username, password, address):
    #Verifico se la coppia username-password esiste nel dataframe
    if (((main_df['Username'] == username) & (main_df['Password'] == password)).any()):
        print("Autenticazione completata")
        #A login effettuato aggiorno l'ip dell'utente e la salvo nel csv
        main_df.at[(main_df['Username'] == username), ['Address']] = address
        main_df.to_csv('register_df.csv', sep=",", encoding='utf-8', index=False)
        UpdateDataFrame()
        return 1
    else:
        print("Password errata o nome utente inesistente")
        return 0