import json, requests, pandas

#getting data from 'COVID-19 Italia' repository
#repo "https://github.com/pcm-dpc/COVID-19.git")

#we need raw files from github
url_nazionale = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale-latest.json'
url_regioni = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json'
url_province = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province-latest.json'
url_storico_nazionale = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv'

#requests library to get a json object from a URL
nazionale_list = requests.get(url_nazionale).json()
regioni_list = requests.get(url_regioni).json()
province_list = requests.get(url_province).json()

#testing: data retrieval 
#print(json.dumps(nazionale_list))
#print(json.dumps(regioni_list))
#print(json.dumps(province_list))

def getNazione():
    print("Nuovi positivi giornalieri per l'intera nazione")
    for i in nazionale_list:
        print ("Nazionale : " + str(i["nuovi_positivi"]))

def getRegione():
    print("Nuovi positivi giornalieri per regione")
    for i in regioni_list:
        print (str(i["denominazione_regione"]) +" : "+ str(i["nuovi_positivi"]))

#i JSON provinciali non contengono il dato sui nuovi contagi giornalieri ma solamente dei casi totali
def getProvincia():
    print("Totale casi per provincia")
    for i in province_list:
        print (str(i["denominazione_provincia"]) +" : "+ str(i["totale_casi"]))

#to get an .R file for daily new cases - library used to process .cvs files = pandas
def getNewCases():
    df = pandas.read_csv(url_storico_nazionale)
    #print(df)
    data = ''
    #I need a counter to get the last date index for later
    count = -1
    #get new positives data
    for i in df["nuovi_positivi"]:
        data = data + str(i) + ', '
        count +=1

    #remove the last two char ', ' 
    data = data[:-2]
    data = '#CONTAGI GIORNALIERI DATO NAZIONALE\nItaly.2020 = c\n(' + data + ')'

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
    # w+ : Opens a file for both writing and reading. Overwrites the existing file if the file exists. If the file does not exist, creates a new file for reading and writing.
    f.write(data)
    f.close()

    #testing data content
    #print(data)

i = input('What do you want to do?\n1) Get daily new case - Nazione \n2) Get daily new cases - Regione\n3) Get total case - Provincia\n4) Save a .R file with daily new cases\nYour selection: ')

if i == '1':
    getNazione()
elif i == '2':
    getRegione()
elif i == '3':
    getProvincia()
elif i == '4':
    getNewCases()
else:
    print ('Wrong input, try again')