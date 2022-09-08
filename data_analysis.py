import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default='notebook'
import seaborn as sns
import statsmodels.api as sm
from sklearn.preprocessing import LabelEncoder 

def render_mpl_table(data, col_width=8.0, row_height=0.825, font_size=8,
                     header_color='#3b5998', row_colors=['#dfe3ee', '#f7f7f7'], edge_color='black',
                     bbox=[0, 0, 1, 1], header_columns=1,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(15)
    
    for k, cell in  six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax

def get_all_data_analysis(df, target):
     
    print(df.info())
    
    describe = df.describe()
    describe=describe.T
    describe=describe.reset_index()
    describe = describe.round(2)
    desc = render_mpl_table(describe, header_columns=0.1, col_width=3.0)
    print(desc)

    count_columns = df.count().reset_index()
    count_columns.rename({0: 'Total_count'}, axis=1, inplace=True)
    unique_values_columns = df.nunique().reset_index()
    unique_values_columns.rename({0: 'Unique_count'}, axis=1, inplace=True)
    duplicate_values = (df.count()-df.nunique()).reset_index()
    duplicate_values.rename({0: 'Duplicate_count'}, axis=1, inplace=True)
    missing_values = df.isnull().sum().reset_index()
    missing_values.rename({0: 'Missing_values'}, axis=1, inplace=True)
    non_missing_values = df.notnull().sum().reset_index()
    non_missing_values.rename({0: 'Non_missing_values'}, axis=1, inplace=True)
    fill_rate = ((1-((df.isnull().sum())/len(df)))*100).reset_index()
    fill_rate.rename({0:"Fill_rate"}, axis=1, inplace=True)
    numerical_analyis = count_columns.merge(unique_values_columns).merge(duplicate_values).merge(missing_values).merge(non_missing_values).merge(fill_rate)
    numerical_analyis=numerical_analyis.round(2)
    num = render_mpl_table(numerical_analyis, header_columns=0.1, col_width=3.0)
    print(num)
    
    # Distribution of target value
    pie = df[target].value_counts().reset_index()
    fig = px.pie(pie, values=target, names="index", title='Distribution of target Value')
    fig.show()
    
    # box plot for outlier detection
    cols=list(df._get_numeric_data().columns)
    for col in cols:
        fig = px.box(df, x=col, color=target, title='Box plot for ' + col + ' outlier detection w.r.t target Value ')
        fig.update_traces(boxpoints='all', jitter=.3)
        fig.show()
        
    # histogram for distribution check
    for col in list(df.columns):
        fig = px.histogram(df, x=col, color=target, title='Histogram for ' + col + ' Distribution w.r.t target Value')
        fig.show()
    
    
    # correlation plot for numerical variables
    plt.figure(figsize=(14,8))
    sns.set_theme(style="white")
    corr = df.corr()
    heatmap = sns.heatmap(corr, annot=True, cmap="Blues", fmt='.1g')
    
    # Stastical summary for classification problem showing many p-value for statastical significance of variables
    x=df[cols]
    y=df[target]
    x = sm.add_constant(x)
    x=x.fillna(0)
    labelencoder= LabelEncoder()
    y = labelencoder.fit_transform(y)
    df=df.fillna(0)
    model = sm.OLS(y,x)
    results = model.fit()
    print(results.summary())

    # pair plot for knowing relationship between all features
    sns.pairplot(df)
    
    
    