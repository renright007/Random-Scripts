from pathlib import Path
import urllib
from numpy.core.numeric import NaN
import pandas as pd
from pandas.io.pytables import IndexCol
from ast import literal_eval
from datetime import datetime
from datetime import date

def otter_file():

    # Load in spreadsheet
    otter_df = pd.read_csv(r'C:/Users/robert.enright/Downloads/Otter/Data_Dump_Global Process Analyst - Recent Active Global Closed Wons.csv')
    
    def format_dates():
        for i in range(0, len(otter_df)):

            otter_df.loc[i, 'First Closed Won Opp Date'] = datetime.strptime(str(otter_df.loc[i, 'First Closed Won Opp Date']), '%m/%d/%Y').strftime('%m/%d/%Y')

            activation_date = str(otter_df.loc[i, 'Activation Date'])

            if activation_date != 'nan':

                try:
                    date_list = activation_date.split('-')
                    new_date = date_list[1] + '/' + date_list[0] + '/20' + date_list[2]
                    activation_date_str = datetime.strptime(new_date, '%b/%d/%Y').strftime('%m/%d/%Y')
                    otter_df.loc[i, 'Activation Date'] = activation_date_str

                except:
                    otter_df.loc[i, 'Activation Date'] = otter_df.loc[i, 'Activation Date'] 
            else:
                otter_df.loc[i, 'Activation Date'] = NaN

            lp_usage_date = str(otter_df.loc[i, 'Last Product usage date'])
        
            if lp_usage_date != 'nan':

                lp_date = datetime.strptime(lp_usage_date, '%m/%d/%Y %H:%M').strftime('%m/%d/%Y')
                otter_df.loc[i, 'Last Product usage date'] = lp_date
        
            else:
                otter_df.loc[i, 'Last Product usage date'] = NaN

    format_dates()
    
    otter_df.to_excel('C:/Users/robert.enright/Downloads/Otter/Data_Dump_Global Process Analyst - Recent Active Global Closed Wons - RE_' + str(date.today()) + '.xlsx', index=True)
    print(otter_df.to_string())
    

otter_file()

