import pandas, os

#   get .CVS file
url_storico_nazionale = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv'

path = 'C:\\Users\\alice\\Desktop\\Tesi\\File\\R PROJECT\\R PROJECT\\R0-master\\data'
#Paste here YOUR DIRECTORY PATH
#path = ''

#changes working directory to save the file where needed
os.chdir(path)

def getNewCases():
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
    #print(data)
    return
 
getNewCases()
