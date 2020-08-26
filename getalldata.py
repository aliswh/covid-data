import os, pandas, datetime, time
import numpy as np

# elapsed time check
t1_start = datetime.datetime.now()

# url
url_storico_nazionale = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv'
url_regioni = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'
url_province = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-' + '20200224' + '.csv'

# method to make lists of the names of regions and provinces
def getNames(url, denominazione):
    dflist = []
    df = pandas.read_csv(url)
    df = df.drop_duplicates(subset=[denominazione])
    dflist = df[denominazione].tolist()
    dflist = [x.replace(' ','') for x in dflist] # remove spaces
    dflist = [x.replace("'",'') for x in dflist] # remove apostrophes
    dflist = [x.replace("-",'') for x in dflist] # remove dashes
    return dflist

# data
data = ''                           # string which stores the number of cases per day - ascending chronological order
allRegion = getNames(url_regioni,'denominazione_regione')        
allProvince = getNames(url_province,'denominazione_provincia')
allProvince = np.delete(allProvince, 4) # 4 is the index of 'In fase di definizione/aggiornamento'
print('\r|O         |')

#time data
today = datetime.date.today()           # get current day
currentTime = time.localtime().tm_hour  # get current hour
n = (today - datetime.date(2020, 2, 22)).days   # number of days from today to the day before the first .csv uploaded
startDate = ''                      # first day in the .cvs file 
lastDate = ''                       # last day in the .cvs file
np.date = []   # list of dates
print('\r|OO        |')

def getDate(count):
    date = today - datetime.timedelta(days=count)
    date = date.strftime('%Y%m%d')
    return date
np.date = []            # list of dates
if currentTime > 18:    # index to decide which day to consider as last day based on current time
    c = 0
else:
    c = 1          
#print('Number of days: ' + str(n))
for i in range(c, n-1): #c, n-1
    np.date.append(getDate(i))
np.date = np.date[::-1]
print('\r|OOO       |')

def makeFile(data, zone):
    if zone in allProvince:
        data = '#CONTAGI GIORNALIERI DATO PROVINCIA: ' + zone +'\n' + zone + '.2020 = c(' + data + ')'
    elif zone in allRegion:
        data = '#CONTAGI GIORNALIERI DATO REGIONE: ' + zone +'\n' + zone + '.2020 = c(' + data + ')'
    else:
        data = '#CONTAGI GIORNALIERI DATO NAZIONALE\n' + zone + '.2020 = c(' + data + ')'

    data = data + '\nnames(' + zone + '.2020)<-seq(from=as.Date("' + startDate + '"), to=as.Date("' + lastDate + '"), by=1)'
    #create new .R file
    filename = zone + ".2020.R"
    f = open(filename, "w+")    #TODO check if 'w+' is the best choice
    f.write(data)
    f.close()
    #print(data)

# 3 funzioni diverse in base alla zona
def nazioneDaily():
    df = pandas.read_csv(url_storico_nazionale)
    data = ''
    count = -1  #I need a counter to get the last date that I need to define lastDate
    for i in df["nuovi_positivi"]:      #get new positives data
        data = data + str(i) + ','
        count +=1
    data = data[:-1]    # delete last ','
    
    #get temporal interval from .csv file - this will be done by the national function but will be used by every file
    global startDate 
    startDate = df["data"][0]
    startDate = startDate[: -9]
    global lastDate 
    lastDate = df["data"][count] #TODO try df["data"][-1] <<< non funziona, prova altro 
    lastDate = lastDate[: -9]

    makeFile(data, 'Italy')

r_df = pandas.read_csv(url_regioni, index_col='denominazione_regione')
r_df.index = r_df.index.str.replace(' ','') # remove spaces
r_df.index = r_df.index.str.replace("'",'') # remove apostrophes
r_df.index = r_df.index.str.replace("-",'') # remove dashes
def regioneDaily(region):
    #dataframe with index column at regional name TODO FARE COME PROVINCE
    df = r_df.loc[region, 'nuovi_positivi'] # r_df = regional dataframe
    count = len(df.index) #get number of rows of  #TODO is this necessary?
    datar = ''

    for i in range(0, count):   #get data from r_df
        datar = datar + str(df.iat[i]) + ','
    datar = datar[:-1]    # delete last ','
    
    makeFile(datar, region)
print('\r|OOOO      |')

# # #   P R O V I N C E   # # #
# main province dataframe
p_df_all = pandas.read_csv(url_province, index_col=['denominazione_provincia'], usecols=['denominazione_provincia'])
p_df_all = p_df_all.drop('In fase di definizione/aggiornamento')  # clear data
p_df_all = p_df_all.drop(p_df_all.loc[p_df_all.index=='Fuori Regione / Provincia Autonoma'].index)
p_df_all.index = p_df_all.index.str.replace(' ','') # remove spaces
p_df_all.index = p_df_all.index.str.replace("'",'') # remove apostrophes
p_df_all.index = p_df_all.index.str.replace("-",'') # remove dashes
def get_p_df_all():
    for date in np.date:  
        global p_df_all
        url_p = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-' + date + '.csv'
        df = pandas.read_csv(url_p, index_col=['denominazione_provincia'], usecols=['denominazione_provincia','totale_casi'])
        df = df.rename(columns={'totale_casi': str(date)})  # rename 'totale_casi' column as the date of the same url
        df = df.drop('In fase di definizione/aggiornamento', axis='rows')   # clear data - keep only provinces names
        df = df.drop(df.loc[df.index=='Fuori Regione / Provincia Autonoma'].index)
        df.index = df.index.str.replace(' ','') # remove spaces
        df.index = df.index.str.replace("'",'') # remove apostrophes
        df.index = df.index.str.replace("-",'') # remove dashes
        p_df_all = p_df_all.join(df, on='denominazione_provincia')    #add new column to the definitive dataframe
get_p_df_all()
print('\r|OOOOO     |')

# provinces .csv files don't have a daily cases column, 
# this function makes this subtraction to obtain it:
    # total cases _minus_ total cases of the day before 
    # _minus_ 
    # total cases of the day before _minus_ total case of the day before yesterday

sub = 0                                 
def totalToDaily(list, prov):
    global sub                          # total cases of the day before _minus_ total case of the day before yesterday --- starts at 0
    start = 0                           # total cases of the day before
    np.returnList = []
    for d in np.date:
        current = p_df_all.loc[prov, d] # total cases 
        dif = current - start           # total cases _minus_ total cases of the day before
        np.returnList.append(dif-sub)   # full subtraction
        sub = dif                       # sets new sub of the day for the next day
    sub=0                               # resets sub for a new province
    return np.returnList

def provinciaDaily(prov):
    df = p_df_all.loc[prov]
    x = df.to_numpy()

    daily = totalToDaily(x, prov)

    datap = '0,' #TODO IMPORTANTE! le province hanno un dato in meno di regione e nazione
    for i in range(0, len(np.date)-1):
        datap = datap + str(daily[i]) + ','
    datap = datap[:-1]
    makeFile(datap, prov)
print('\r|OOOOOO    |')

def changeDir():
    dataDir = os.path.dirname(os.path.realpath('__file__'))
    # To access the file inside a sibling folder
    path = '../data'
    path = os.path.join(dataDir, path)
    #filename = os.path.join(fileDir, '../[sibling directory]')
    path = os.path.abspath(os.path.realpath(path))
    os.chdir(path)
changeDir()    #change working directory

# new file with names of all .R files
f = open('zones_list', 'w')
f.write('Italy'+'\n')
for name in allRegion:
    f.write(name + '\n')
for name in allProvince:
    f.write(name + '\n')
f.close()
print('\r|OOOOOOO   |')

nazioneDaily()  #funzione che salva il file aggiornato - nazionale
print('\r|OOOOOOOO  |')

for x in allRegion:     #funzione che salva il file aggiornato - regionale
    regioneDaily(x)
print('\r|OOOOOOOOO |')

for x in allProvince:   #funzione che salva il file aggiornato - provinciale
    provinciaDaily(x)
print('| - DONE - |\n')

# elapsed time check
t1_stop = datetime.datetime.now()  
print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)