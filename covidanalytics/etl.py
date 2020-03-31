import pandas as pd

def covid_csv_to_df(csv_path):
    df = pd.read_csv(csv_path)
    df.rename(columns={'Country/Region':'Country_Region','Province/State':'Province_State'},inplace=True)
    df.fillna('None',inplace=True)
    return df

def covid_province_state(covid_df,province_state):
    covid_df['Confirmed'].replace(to_replace='None',value=0,inplace=True)
    covid_df['Deaths'].replace(to_replace='None',value=0,inplace=True)
    covid_df['Recovered'].replace(to_replace='None',value=0,inplace=True)
    q_str = 'Province_State=="{pr}"'.format(pr=province_state)
    con=covid_df.query(q_str).sum(axis=0)['Confirmed']
    dea=covid_df.query(q_str).sum(axis=0)['Deaths']
    rec=covid_df.query(q_str).sum(axis=0)['Recovered']
    act=con - (dea + rec)
    try:
        if 'Last_Update' in covid_df.keys():
            dat=covid_df.query(q_str)['Last_Update'].values[0]
            dat=dat.split(' ')[0]
        elif 'Last Update' in covid_df.keys():
            dat=covid_df.query(q_str)['Last Update'].values[0]
            dat=dat.split('T')[0]
    except:
        dat='NA'
    return {'province_state':province_state,
            'confirmed':con,
            'deaths':dea,
            'active':act,
            'date':dat}

def covid_country_region(covid_df,country_region):
    covid_df['Confirmed'].replace(to_replace='None',value=0,inplace=True)
    covid_df['Deaths'].replace(to_replace='None',value=0,inplace=True)
    covid_df['Recovered'].replace(to_replace='None',value=0,inplace=True)
    q_str = 'Country_Region=="{cr}"'.format(cr=country_region)
    con=covid_df.query(q_str).sum(axis=0)['Confirmed']
    dea=covid_df.query(q_str).sum(axis=0)['Deaths']
    rec=covid_df.query(q_str).sum(axis=0)['Recovered']
    act=con - (dea + rec)
    try:
        if 'Last_Update' in covid_df.keys():
            dat=covid_df.query(q_str)['Last_Update'].values[0]
            dat=dat.split(' ')[0]
        elif 'Last Update' in covid_df.keys():
            dat=covid_df.query(q_str)['Last Update'].values[0]
            dat=dat.split('T')[0]
    except:
        dat='NA'
    return {'country_region':country_region,
            'confirmed':con,
            'deaths':dea,
            'active':act,
            'date':dat}

def covid_query(covid_df,query_str):
    covid_df['Confirmed'].replace(to_replace='None',value=0,inplace=True)
    covid_df['Deaths'].replace(to_replace='None',value=0,inplace=True)
    covid_df['Recovered'].replace(to_replace='None',value=0,inplace=True)
    q_str = query_str
    con=covid_df.query(q_str).sum(axis=0)['Confirmed']
    dea=covid_df.query(q_str).sum(axis=0)['Deaths']
    rec=covid_df.query(q_str).sum(axis=0)['Recovered']
    act=con - (dea + rec)
    try:
        if 'Last_Update' in covid_df.keys():
            dat=covid_df.query(q_str)['Last_Update'].values[0]
            dat=dat.split(' ')[0]
        elif 'Last Update' in covid_df.keys():
            dat=covid_df.query(q_str)['Last Update'].values[0]
            dat=dat.split('T')[0]
    except:
        dat='NA'
    return {'query':query_str,
            'confirmed':con,
            'deaths':dea,
            'active':act,
            'date':dat}

def dates_to_filenames(start_date,end_date):
    date_range = pd.date_range(start=start_date,end=end_date)
    reports = []
    for d in date_range:
        dt = str(d).split(' ')[0]
        yr = dt.split('-')[0]
        mn = dt.split('-')[1]
        dy = dt.split('-')[2]
        fname = mn + '-' + dy + '-' + yr + '.csv'
        reports.append(fname)
    return reports
