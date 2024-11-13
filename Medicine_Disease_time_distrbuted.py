# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 23:49:09 2023

@author: USER
"""

import pandas as pd
import re

Medicine_list=[]

Medicine_1 = pd.read_csv("D:/Landseed_medicine/Frist_X0_11(4).csv")#78050所使用藥物
icd9 = pd.read_csv("D:/Landseed_medicine/landseed_first_time_icd9.csv")#78050患者確診其他疾病紀錄

Medicine_2 = Medicine_1.rename(columns = {"landseedID":"ID","INDATE":"date"})
Medicine_3 = Medicine_2.loc[:, ['ID','ATC_CODE','date']]#選取特定欄位
Medicine_3['ID'] = Medicine_3['ID'].astype(str)
icd9_2 = icd9.loc[:, ['ID','icd9','date']]
icd9_2['ID'] = icd9_2['ID'].astype(str)

p = re.compile('\AA10')
Medicine = Medicine_3.loc[Medicine_3["ATC_CODE"].str.contains(p)]
Medicine = Medicine.drop_duplicates(subset=['ID'])
    
Disease_list=[]
Disease = open('C:/Users/USER/Desktop/25002_A10/25002_chi/25002_chi_list.csv','r',encoding='UTF-8')
for row in Disease:
    row1=row.lstrip('\ufeff')
    row2=row1.rstrip()
    Disease_list.append(row2)
for D in Disease_list:
    print(D)
    icd9_3 = icd9_2.loc[icd9_2['icd9']==D]
    icd9_4 = icd9_3.drop_duplicates(subset=['ID'])
    Medicine_ID = Medicine["ID"]
    Medicine_ID = Medicine_ID.tolist()#sreies to list
    #sleep_Medicine_LEVOCETIRIZINE_ID = list(map(str,sleep_Medicine_LEVOCETIRIZINE_ID))#int of list to str of list
    icd9_ID = icd9_4["ID"]
    icd9_ID_1 = icd9_ID.tolist()
    #icd9_36610_ID = list(map(str,icd9_36610_ID))
    Medicine_icd9_ID = list(set(Medicine_ID) & set(icd9_ID_1))#a list and b list 交集
    print(Medicine_icd9_ID)
    if len(Medicine_icd9_ID)>0:
        Medicine1 = pd.DataFrame()
        icd91 = pd.DataFrame()

        for i in Medicine_icd9_ID:
            Medicine_date = Medicine.loc[Medicine["ID"]==i]
            Medicine1 = Medicine1.append(Medicine_date)
            icd9_date = icd9_4.loc[icd9_4["ID"]==i]
            icd91 = icd91.append(icd9_date)
            Medicine3 = Medicine1.reset_index(drop=True)#去除index #.set_index(將欄位設定為index)
            icd91 = icd91.reset_index(drop=True)

        Medicine3["date"] = Medicine3["date"].astype(str)#dataframe轉換欄位型態
        Medicine3["ID"] = Medicine3["ID"].astype(str)
        Medicine4 = Medicine3.drop(['ID'],axis = 1)
        Medicine4["date"] = pd.to_datetime(Medicine4["date"])#文字轉時間
        Medicine5 = Medicine4.sort_values(by="date")#由時間小到大排序
        Medicine6 = Medicine5.set_index('date')#將date設定為index
        Medicine7 = Medicine6.groupby(['date']).count()#統計有多少相同值
        Medicine8 = Medicine7.rename(columns = {"ATC_CODE":"Medicine_Number"})#改columns name
        
        Medicine1_year = Medicine8.resample('AS').sum().to_period('A')# "AS"是每年第一天为开始日期, "A是每年最后一天,計算一年累計多少人
        Medicine1_year = Medicine1_year.rename_axis('date').reset_index()#index改到colums
        Medicine1_year['date'] = Medicine1_year['date'].dt.strftime('%Y')#時間格式改文字

        Medicine1_month = Medicine8.resample('M').sum().to_period('M')# 按月度统计并显示
        Medicine1_month = Medicine1_month.rename_axis('date').reset_index()
        Medicine1_month['date'] = Medicine1_month['date'].dt.strftime('%Y-%m')



        icd91["date"] = icd91["date"].astype(str)
        icd91["ID"] = icd91["ID"].astype(str)
        icd93 = icd91.drop(['ID'],axis = 1)
        icd93["date"] = pd.to_datetime(icd93["date"])
        icd94 = icd93.sort_values(by="date")
        icd95 = icd94.set_index('date')
        icd96 = icd95.groupby(['date']).count()
        icd97 = icd96.rename(columns = {"icd9":"Disease_Number"})
            
        icd91_year = icd97.resample('AS').sum().to_period('A')
        icd91_year = icd91_year.rename_axis('date').reset_index()
        icd91_year['date'] = icd91_year['date'].dt.strftime('%Y')

        icd91_month = icd97.resample('M').sum().to_period('M')
        icd91_month = icd91_month.rename_axis('date').reset_index()
        icd91_month['date'] = icd91_month['date'].dt.strftime('%Y-%m')



        Medicine_icd9_year = pd.merge(Medicine1_year,icd91_year,how='outer',left_on=Medicine1_year['date'],right_on=icd91_year['date'])#資料合併
        Medicine_icd9_year = Medicine_icd9_year.drop('date_x',axis = 1)
        Medicine_icd9_year = Medicine_icd9_year.drop('date_y',axis = 1)
        Medicine_icd9_year = Medicine_icd9_year.rename(columns = {"key_0":"date(year)"})
        Medicine_icd9_year = Medicine_icd9_year.fillna(0)
        print(Medicine_icd9_year)
        Medicine_len = len(Medicine_icd9_year)
        if Medicine_len > 4:
            #out ='{}'.format(M)
            #f.write(out+'\n')
            Medicine_icd9_year.to_csv("C:/Users/USER/Desktop/25002_A10/25002_date_distrbuted_number/Year/"+D+"_A10單位時間累計人數(Year).csv",encoding='UTF-8')
    
    


        Medicine_icd9_month = pd.merge(Medicine1_month,icd91_month,how='outer',left_on=Medicine1_month['date'],right_on=icd91_month['date'])
        Medicine_icd9_month = Medicine_icd9_month.drop('date_x',axis = 1)
        Medicine_icd9_month = Medicine_icd9_month.drop('date_y',axis = 1)
        Medicine_icd9_month = Medicine_icd9_month.rename(columns = {"key_0":"date(month)"})
        Medicine_icd9_month = Medicine_icd9_month.fillna(0)
        print(Medicine_icd9_month)
        Medicine_len = len(Medicine_icd9_month)
        if Medicine_len > 4:
            Medicine_icd9_month.to_csv("C:/Users/USER/Desktop/25002_A10/25002_date_distrbuted_number/Month/"+D+"_A10單位時間累計人數(Month).csv",encoding='UTF-8')