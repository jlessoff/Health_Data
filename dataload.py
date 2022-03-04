from pytrends.request import TrendReq
import pandas as pd
import time
import random
from matplotlib import pyplot as plt
# for list of key words, interest over time in given period for regional level
pytrends = TrendReq(hl='en-US', tz=360)
from datetime import date


#GOOGLE DATA
pytrends.build_payload(kw_list=['covid','coronavirus'], timeframe=f'2020-02-26 {date.today()}', geo='US')
regiondf = pytrends.interest_by_region()
df_ibr =pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)
related_queries = pytrends.related_queries()
related_queries.values()
df_rq = list(related_queries.values())[0]['rising']
dfrising = pd.DataFrame(df_rq).head(20)
keywords=dfrising['query'].tolist()
kw_list=pd.read_csv('google.csv')
kw_list=kw_list['0'].values.tolist()
key_words=kw_list+keywords
print(key_words)
df_us_states=pd.read_csv('us_states.csv',header=None)
df_us_states.rename(columns={0:'state'},inplace=True)
us_states=df_us_states['state'].to_list()
us_states=us_states
tmp = pd.DataFrame()
print(key_words)
for j in us_states:
    for i in key_words:
        pytrends.build_payload(kw_list=[i],timeframe=f'2020-02-26 {date.today()}', geo=j)
        pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)
        time_df = pytrends.interest_over_time()
        time_df.rename(columns={i: 'number'}, inplace=True)
        time_df['keyword']=i
        time_df['state']=j
        tmp = tmp.append(time_df)
        time.sleep(20.75 + random.random())
plt.title(j, fontweight='bold')
tmp.to_csv('google_data.csv', index=True, header=False)


##COVID DATA USA
covid_daily = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
dates = covid_daily.columns[11:]
confirmed_df_long = covid_daily.melt(
    id_vars=['Province_State', 'Country_Region','Admin2'],
    value_vars=dates,
    var_name='Date',
    value_name='Confirmed'
)
us_covid_df=confirmed_df_long.groupby([ 'Province_State','Date']).sum().reset_index()
us_covid_df['Date']=pd.to_datetime(us_covid_df['Date'])
us_covid_df['week']=us_covid_df['Date'].dt.strftime('%Y-w%U')
us_covid_df=us_covid_df.groupby(by=['Province_State','week']).sum()
