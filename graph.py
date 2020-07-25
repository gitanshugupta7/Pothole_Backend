import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns

def plotting(diction):

    print(diction)
    rows = list()
    element = dict()
    for key,val in diction.items():
        for i in val:
            element['Date'] = key
            element['Ward'] = i
            if(type(val[i]['complaints_registered']) is None):
                element['Registered'] = 0
            else:
                element['Registered'] = val[i]['complaints_registered']
            if(type(val[i]['complaints_completed']) is None):
                element['Completed'] = 0
            else:
                element['Completed'] = val[i]['complaints_completed']
            #print("For ward ",i," complaints registered are ",val[i]['complaints_registered'])
            #print("For ward ",i," complaints completed are ",val[i]['complaints_completed'])
            rows.append(element)
            element=dict()

    #print("\n\n",rows,"\n\n")
    df = pd.DataFrame(rows)

    df.columns = ['Date' , 'Ward' , 'Complaints_Registered' , 'Complaints_Completed']

    fig=px.bar(x=df['Ward'],y=df['Complaints_Registered'])
    fig.update_layout(title="Distribution of Number of Registered Cases",xaxis_title="Wards",yaxis_title="Number of Cases")
    fig.show()
    
    
