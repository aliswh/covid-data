import os, pandas

file = 'Italy.2020.R'

#url
url_storico_nazionale = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv'
url_regioni = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'

#arrays
allRegion = {}
allProvince = {}

# 3 funzioni diverse in base alla zona
def nazioneDaily():
    df = pandas.read_csv(url_storico_nazionale)
    data = ''
    #I need a counter to get the last date that I need later
    count = -1
    #get new positives data
    for i in df["nuovi_positivi"]:
        data = data + str(i) + ','
        count +=1

    data = data[:-1]
    data = '#CONTAGI GIORNALIERI DATO NAZIONALE\nItaly.2020 = c(' + data + ')'

    #get temporal interval from CVS file
    startDate = df["data"][0]
    startDate = startDate[: -9]
    #modify this line and delete'#' if you want a specific start date
    #startDate = 'YYYY-MM-DD'

    lastDate = df["data"][count]
    lastDate = lastDate[: -9]
    #modify this line and delete'#' if you want a specific last date
    #lastDate = 'YYYY-MM-DD'

    data = data + '\nnames(Italy.2020)<-seq(from=as.Date("' + startDate + '"), to=as.Date("' + lastDate + '"), by=1)'

    #create new .R file
    f = open("Italy.2020.R", "w+")
    f.write(data)
    f.close()

    #testing data content
    print(data)
    return

def regioneDaily(region):
    #dataframe with index column at regional name
    df = pandas.read_csv(url_regioni, index_col='denominazione_regione')

    # r_df = regional dataframe
    r_df = df.loc[region, 'nuovi_positivi']
    #print(r_df)

    count = len(r_df.index) #get number of rows of 
    data = ''   #empty string - will be the data for the .R file

    for i in range(0, count):   #get data from r_df
        data = data + str(r_df.iat[i]) + ','

    data = data[:-1]
    data = '#CONTAGI GIORNALIERI DATO REGIONE: ' + region +'\n' + region + '.2020 = c(' + data + ')'

    # to get the first and last date, create a dataframe 'date_df' with only the first and last entry of 'df'
    date_df = df.iloc[[0, -1]]
    #get temporal interval from CVS file
    startDate = date_df["data"][0]
    startDate = startDate[: -9]
    #modify this line and delete'#' if you want a specific start date
    #startDate = 'YYYY-MM-DD'

    lastDate = date_df["data"][1]
    lastDate = lastDate[: -9]
    #modify this line and delete'#' if you want a specific last date
    #lastDate = 'YYYY-MM-DD'

    data = data + '\nnames(' + region + '.2020)<-seq(from=as.Date("' + startDate + '"), to=as.Date("' + lastDate + '"), by=1)'

    #create new .R file
    filename = region +".2020.R"
    f = open(filename, "w+")
    f.write(data)
    f.close()

    #testing data content
    print(data)
    return


#TODO don't go in a new directory for every file, change it one time only

# !!! li salva in code non in data
def changeFile():
    dataDir = os.path.dirname(os.path.realpath('__file__'))
    print(dataDir) #TODO test
    #For accessing the file inside a sibling folder. TODO write what it does
    path = '../data'
    path = os.path.join(dataDir, path)
    #filename = os.path.join(fileDir, '../[sibling directory]')
    path = os.path.abspath(os.path.realpath(path))
    os.chdir(path)
    print(path) #test

#change working directory
changeFile() 
#funzione che salva il file aggiornato - nazionale
nazioneDaily()
#funzione che salva il file aggiornato - regionale
regioneDaily()
#funzione che salva il file aggiornato - provinciale
#provinciaDaily()