import requests
import json
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import regex as re 
import statsmodels.api as sm
import statsmodels.formula.api as smf

def getjson_fda_arms(key,year,variable,statecode,category,report,farmtype):
    """
    Returns pandas dataframe containing result from the FDA ARMS Database
    
    Parameters
    ----------
    key : API key which can be applied from the FDA ARMS webpage
    year : List of years for which you want the data
    variable_id: list of variable ids for desired variable
    statecode: code of the state 
    category: list of category codes of the data you want
    report: list of codes of reports you want data from
    farmtype: string of farmtype
    
    Returns
    --------
    dictionary object of the requested API
    
    Example
    --------
    
    >>> key = '91ycY1QG2K2gtDXnvHqwB1EvpN8WdKVGEBTLPZSf'
    >>> year = ['2000','2001','2002','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021']
    >>> variable = ['kount','crop']
    >>> category = ['sal']
    >>> report = ['3']
    >>> farmtype = 'all farms'
    >>> statewide = ['12','13']
    >>> example = getjson_fda_arms(key,year,variable,statecode,category,report,farmtype)
    >>> type(example)
    dict"""
    try:
        year1 = ",".join(year)
        variable1 = ",".join(variable_id)
        statecode1 = ",".join(statecode)
        category1 = ",".join(category)
        report1 = ",".join(report)
        farmtype1 = re.sub(' ','+',farmtype)
        url = 'https://api.ers.usda.gov/data/arms/surveydata?api_key='
        print(url)
        arms_request = url + key + '&variable' + variable1 +'&year='+ year1 +'&state='+ statecode1 +'&report='+ report1 +'&category='+ category1 +'&farmtype='+ farmtype1
        r = requests.get(arms_request).json()
        b = r['data']
        return(r)

    except: print('Please check your input values')

def stateid(key):
    """
    Prints the codes and list of states for which FDA ARMS data is available
    
    Parameters
    ----------
    key:API key which can be applied from the FDA ARMS webpage
    
    Example
    --------

    >>> stateid('your_key')
           id  code               name
        0   00  all  All survey states
        1   05   ar           Arkansas
        2   06   ca         California
        3   12   fl            Florida
        4   13   ga            Georgia
        5   17   il           Illinois
        6   18   in            Indiana
        7   19   ia               Iowa
        8   20   ks             Kansas
        9   27   mn          Minnesota
        10  29   mo           Missouri
        11  31   ni           Nebraska
        12  37   nc     North Carolina
        13  48   tx              Texas
        14  53   wa         Washington
        15  55   wi          Wisconsin"""
    try:
        url = 'https://api.ers.usda.gov/data/arms/state?api_key=' + key
        r = requests.get(url).json()
        a = r['data']
        df = pd.DataFrame.from_records(a)
        print(df)
    except: print('Check Key')

def timesseries_regplot(df,variable_id,state,category_value):
    """
    Prints time series regression summary and plots regression line for a select variable
    
    Parameters
    ----------
    df : output from the function getdf_fda_arms()
    variable_id: string of variable id of interest
    state: name of state of interest
    category_value: string containing category_value of interest
    
    Returns
    --------
    Prints the summary of time series regression and the plot of the same"""
    try:
        df2 = df.loc[(df['variable_id'] == variable_id)& (df['state']== state)&(df['category_value']== category_value)]
        lm = smf.ols('estimate ~ year ', data = df2).fit()
        print(lm.summary())
        sns.set_style("ticks",{'axes.grid' : True})
        sns.scatterplot(x = 'year', y = 'estimate',data = df2)
        sns.regplot(x = 'year', y = 'estimate', data = df2, 
                    scatter = True, ci = None, fit_reg = True, color = 'b')
    except: print('Check input values')

def getdf_fda_arms(key,year,variable,statecode,category,report,farmtype):
    """
    Returns pandas dataframe containing result from the FDA ARMS Database
    
    Parameters
    ----------
    key : API key which can be applied from the FDA ARMS webpage
    year : List of years for which you want the data
    variable_id: list of variable ids for desired variable
    statecode: code of the state 
    category: list of category codes of the data you want
    report: list of codes of reports you want data from
    farmtype: string of farmtype
    
    Returns
    --------
    dictionary object of the requested API
    
    Example
    --------
    
    >>> key = '91ycY1QG2K2gtDXnvHqwB1EvpN8WdKVGEBTLPZSf'
    >>> year = ['2000','2001','2002','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021']
    >>> variable = ['kount','crop']
    >>> category = ['sal']
    >>> report = ['3']
    >>> farmtype = 'all farms'
    >>> statecode = ['12','13']
    >>> example = getdf_fda_arms(key,year,variable,statecode,category,report,farmtype)
    >>> type(example)
    pandas.core.frame.DataFrame"""
    try:
        year1 = ",".join(year)
        variable1 = ",".join(variable)
        statecode1 = ",".join(statecode)
        category1 = ",".join(category)
        report1 = ",".join(report)
        farmtype1 = re.sub(' ','+',farmtype)
        url = 'https://api.ers.usda.gov/data/arms/surveydata?api_key='
        arms_request = url + key + '&variable' + variable1 +'&year='+ year1 +'&state='+ statecode1 +'&report='+ report1 +'&category='+ category1 +'&farmtype='+ farmtype1
        r = requests.get(arms_request).json()
        b = r['data']
        df = pd.DataFrame.from_records(b)
        return(df)
    except: 
        print('Please check your input values')

def plotseries_cat(df,variable_id,state):
    """
    Plots a variable of interest over time by category value
    
    Parameters
    ----------
    df : output from the function getdf_fda_arms()
    variable_id: string of variable id of interest
    state: name of state of interest
    
    Returns
    --------
    Timeseries plot of a variable of interest by category of interest.
    
    Example
    --------
    
    >>> plotseries_cat(df,variable_id='freconum',state='Florida')"""
    try:
        df2 = df.loc[(df['variable_id'] == variable_id) & (df['state']== state)]
        fig, a = plt.subplots()
        for key, data in df2.groupby('category_value'):
            data.plot(x='year', y='estimate', ax=a, label=key)
    except: print('Check input values')

def farmtype(key):
    """
    Prints the codes for farmtype from FDA ARMS
    
    Parameters
    ----------
    key:API key which can be applied from the FDA ARMS webpage
    
    Example
    --------

    >>> farmtype('your_key')
           id                      name  desc  is_invalid
        0   1                 All Farms  None       False
        1   2           Farm Businesses  None       False
        2   3  Farm Operator Households  None       False"""
    try:    
        url = 'https://api.ers.usda.gov/data/arms/farmtype?api_key=' + key
        r = requests.get(url).json()
        a = r['data']
        df = pd.DataFrame.from_records(a)
        print(df)
    except: print('Check Key')