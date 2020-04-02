import pandas as pd
import numpy as np
import sklearn
import sklearn.linear_model as lm

def covid_dict_to_timeseries_df(ps_dict,start_date,end_date):
    df=pd.DataFrame(ps_dict,index=pd.date_range(start_date,end_date))
    df['total_change'] = np.zeros((len(df.index),1))
    df['percent_change'] = np.zeros((len(df.index),1))
    df['7day_fit_m'] = np.zeros((len(df.index), 1))
    final = df['confirmed'].loc[df.index[1]:df.index[-1]].values
    initial = df['confirmed'].loc[df.index[0]:df.index[-2]].values
    tc = final - initial
    tc = np.insert(tc,0,0)
    df['total_change'] = tc
    #check for zero in demon
    idx=np.where(initial == 0)
    if idx[0].size!=0:
        denom = initial[np.where(initial==0)]=np.nan
    pc = ((final - initial) / initial) * 100
    pc = np.insert(pc,0,0)
    df['percent_change'] = pc
    df.fillna(0, inplace=True)
    #calc 7d fits
    if df.shape[0] >= 14:
        for i in range(0, (df.shape[0] - 7)):
            if i == 0:
                mb = daily_lin_fit(7, df['confirmed'][-7::].values)
                df.at[df.index[-1], '7day_fit_m'] = mb['m']
            else:
                mb = daily_lin_fit(7, df['confirmed'][((i * -1) - 7):(i * -1)].values)
                df.at[df.index[((i + 1) * -1)], '7day_fit_m'] = mb['m']

    return df

def daily_lin_fit(n_days,y_vals):
    day_idx = n_days + 1
    x = np.arange(1, day_idx)
    x = x.reshape(-1, 1)
    y = y_vals
    lin_fit = lm.LinearRegression(fit_intercept=True).fit(x, y)
    coefs = {'m': lin_fit.coef_[0],
             'b': lin_fit.intercept_}
    return coefs
