import pandas as pd
import numpy as np

def covid_dict_to_timeseries_df(ps_dict,start_date,end_date):
    df=pd.DataFrame(ps_dict,index=pd.date_range(start_date,end_date))
    df['total_change'] = np.zeros((len(df.index),1))
    df['percent_change'] = np.zeros((len(df.index),1))
    final = df['confirmed'].loc[df.index[1]:df.index[-1]].values
    initial = df['confirmed'].loc[df.index[0]:df.index[-2]].values
    tc = final - initial
    tc = np.insert(tc,0,0)
    df['total_change'] = tc
    denom = initial[np.where(initial==0)]=np.nan
    pc = ((final - initial) / initial) * 100
    pc = np.insert(pc,0,0)
    df['percent_change'] = pc
    df.fillna(0,inplace=True)
    return df
