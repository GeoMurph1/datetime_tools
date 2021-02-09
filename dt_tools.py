# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 09:37:35 2021

@author: Michael
"""
import pandas as pd
from datetime import datetime, timedelta

def round_datetimes(df):
    """
    

    Parameters
    ----------
    df : pandas dataframe containing datetime-like array "date_time"

    Returns
    -------
    DataFrame with same length with date time column reduced to minute ('date_time_short'), time delta ('time_delta'),
    and new datetime column rounded to nearest whole minute ('dt_round_min')

    """
    df['date_time'] = pd.to_datetime(df['date_time'])
    df["date_time"] = df.date_time.dt.strftime('%Y%m%d %H:%M:%S')
    df['date_time'] = pd.to_datetime(df['date_time'])
    df.sort_values(by='date_time', inplace=True)
    df["date_time_short"] = df.date_time.dt.strftime('%Y%m%d %H:%M')
    df["date_time_short"] = pd.to_datetime(df["date_time_short"])
    df["date_time_date"] = df.date_time.dt.strftime('%Y%m%d')
    df["date_time_date"] = pd.to_datetime(df["date_time_date"], format='%Y%m%d')
    df['time_delta'] = df["date_time"] - df.date_time_short
    df['dt_round_min'] = df["date_time_short"]
    df.loc[df.time_delta > timedelta(seconds=30), 'dt_round_min'] = df["date_time_short"] + timedelta(minutes=1)
    df['dt_round_min'] = pd.to_datetime(df['dt_round_min'])
    return df

def bd_bt_filter(df):
    """

    Parameters
    ----------
    df : Cleaned dataframe with standardized columns

    Returns
    -------
    df : DataFrame with data from business days only between 7AM and 5PM

    """
    df['date_time'] = pd.to_datetime(df['date_time'])
    df['time_start'] = datetime.strptime('07:00:00', '%H:%M:%S').time()
    df['time_end'] = datetime.strptime('17:00:00', '%H:%M:%S').time()
    df['time'] = df.date_time.dt.time
    df['day'] = df.date_time.dt.weekday
    df = df.loc[(df.day < 5) & ((df.time >= df.time_start) & (df.time <= df.time_end))]
    df.drop(columns=['time_start', 'time_end', 'time', 'day'], inplace=True)
    return df