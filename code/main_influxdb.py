# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 14:45:44 2021

@author: Mylee
"""

from influxdb import InfluxDBClient
from time import sleep
from socket import getaddrinfo, AF_INET, gethostname
import os
import pandas as pd
from datetime import datetime
import time
from calendar import timegm
import progressbar

#for ip in getaddrinfo(host=gethostname(), port=None, family=AF_INET):
#    print(ip[4][0])

client = InfluxDBClient(host='10.0.0.46', port=8086, database='challenger')
client.create_database('challenger')


def ReadFileAndSendData(MyFileName, MyDataBase):
    print('--- Sending ' + MyFileName + ' data to the Database ---')
    print(os.getcwd())
    MyFullPath = os.getcwd() + "/" + MyFileName #TA7F.csv"

    MyData = pd.read_csv(MyFullPath, delimiter=',')
    print(MyData)

    bar = progressbar.ProgressBar(max_value=len(MyData[0:]))

    data=[]
    #for ii in range(len(Data_Legload_PS_fore[0:])-0):
    for ii in progressbar.progressbar(range(len(MyData[0:])-0), redirect_stdout=True):
        #utc_time = datetime.strptime(Data_CraneLoad_CraneOn.iat[ii, 0], "%Y-%m-%d %H:%M:%S")
        #epoch_time= (utc_time-datetime(1970,1,1)).total_seconds()
        #try:
        #    utc_time = time.strptime(Data_Legload_PS_fore.iat[ii, 0], "%Y-%m-%d %H:%M:%S.%f")
        #except:
        #    utc_time = time.strptime(Data_Legload_PS_fore.iat[ii, 0], "%Y-%m-%d %H:%M:%S")
        #epoch_time = timegm(utc_time)

        columnCounter=0
        for columnName in MyData.columns.values:
            if columnName == 'Time': continue

            columnName = columnName.replace(".", "_")

            #print(columnName)
       #     try:
                #print(MyFileName[-8:-5] + '_' + columnName + ',Vessel=Plus3600 value=' + str(MyData.iat[ii, columnCounter]) + ' ' + str(int(MyData.iat[ii, 0]/1000000000)))
                # MyFileName[-8:-5] to get the same tagnames for all leg positions. The distinction between the leg positions is made in the database name.
                # this has the advantage that one can use parameters in Grafana!
        #        data.append(columnName + ',Vessel=Plus3600 value=' + str(MyData.iat[ii, columnCounter]) + ' ' + str(int(MyData.iat[ii, 0]/1000000000)))

         #   except ValueError as ve:
          #      print("Error on data on line " + str(ii))
           #     print(ve)

            columnCounter=columnCounter+1
        if ii%100001==0:
            client.write_points(data, database=MyDataBase, time_precision='s', batch_size=10000, protocol='line')
            data=[]
    #next line still needs to execute for the remainder
    client.write_points(data, database=MyDataBase, time_precision='s', batch_size=10000, protocol='line')

    print('--- Finished sending ' + MyFileName + ' data to the Database ---')


if __name__ == "__main__":
    print('--- Running main from: ---')
    print(os.getcwd() + "\Data")
    for myFile in os.listdir(os.getcwd()+ "/"):
        print(myFile)
        #ReadFileAndSendData(myFile)

    ReadFileAndSendData("CombinedAndCleaned.csv", "challenger")
