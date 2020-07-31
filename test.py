import pandas

url_regioni = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'

regione = input('>')

def regioneDaily(regione):
    #dataframe with index column at regional name
    df = pandas.read_csv(url_regioni, index_col='denominazione_regione')

    region = regione

    # r_df = regional dataframe
    r_df = df.loc[region, 'nuovi_positivi']
    print(r_df)

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

    print('data')
    print(data)

regioneDaily(regione)