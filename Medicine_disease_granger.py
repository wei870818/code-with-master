# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 22:07:50 2023

@author: USER
"""
import pandas as pd
from statsmodels.stats.diagnostic import unitroot_adf
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.stattools import coint
from collections import Counter

Test_result_value_1 = []

Disease_list = []
Disease = open('C:/Users/USER/Desktop/25002_A10/25002_chi/25002_chi_list.csv','r',encoding='UTF-8')
for row in Disease:
    row1=row.lstrip('\ufeff')
    row2=row1.rstrip()
    Disease_list.append(row2)
for D in Disease_list:
    print(D)
    df =pd.read_csv("C:/Users/USER/Desktop/25002_A10/25002_date_distrbuted_number/Month/A10_"+D+"單位時間累計人數(Month).csv", parse_dates=['date(month)'],encoding='UTF-8')
    df = df.set_index('date(month)')
    df = df.sort_index(ascending=True)
    df = df.drop(['Unnamed: 0'],axis = 1)
    df_count_ATC_CODE = Counter(df['Medicine_Number']).most_common(1)
    df_count_ATC_CODE = df_count_ATC_CODE[0]
    #if df_count_ATC_CODE[1] < 4 :
    #    df_count_Disease_Number = Counter(df['Disease_Number']).most_common(1)
    #    df_count_Disease_Number = df_count_Disease_Number[0]
    #    if df_count_Disease_Number[1] < 4:
        
    Test_result_value = []
    Medicine_Disease = D
    Test_result_value.append(Medicine_Disease)
    #Test_result_value.append(D)
        
    print("原始資料時間平穩檢驗")
    unitroot_adf_Medicine = unitroot_adf(df['Medicine_Number'])#單位根平穩性檢驗
    unitroot_adf_Disease = unitroot_adf(df['Disease_Number'])
    Medicine_adf = str(unitroot_adf_Medicine[1])
    Disease_adf = str(unitroot_adf_Disease[1])

    Test_result_value.append(Medicine_adf)
    Test_result_value.append(Disease_adf)
            
    print("藥物時間平穩性pvalue :",unitroot_adf_Medicine[1])
    print("疾病時間平穩性pvalue :",unitroot_adf_Disease[1])

    print("原始資料做格蘭傑")
    Medicine_granger = grangercausalitytests(df[['Disease_Number','Medicine_Number']], maxlag=1,addconst=True,verbose=True)#原始資料直接做格蘭傑
    Disease_granger = grangercausalitytests(df[['Medicine_Number','Disease_Number']], maxlag=1)
                
    Medicine_granger = Medicine_granger[1]
    Medicine_granger = Medicine_granger[0]
    Medicine_granger = Medicine_granger['ssr_chi2test']
    Medicine_granger = str(Medicine_granger[1])

    Disease_granger = Disease_granger[1]
    Disease_granger = Disease_granger[0]
    Disease_granger = Disease_granger['ssr_chi2test']
    Disease_granger = str(Disease_granger[1])
    Test_result_value.append(Medicine_granger)
    Test_result_value.append(Disease_granger)
        
    print("一階差分")
    Medicine_Disease_diff_1 = df.diff(periods = 1)#一階插分將時間從不平穩到平穩
    Medicine_Disease_diff_1 = Medicine_Disease_diff_1.fillna(0)
    Medicine_diff_1 = unitroot_adf(Medicine_Disease_diff_1['Medicine_Number'])#一階插分檢驗平穩
    Disease_diff_1 = unitroot_adf(Medicine_Disease_diff_1['Disease_Number'])
    Medicine_diff_1 = Medicine_diff_1[1]
    Disease_diff_1 = Disease_diff_1[1]
    Test_result_value.append(Medicine_diff_1)
    Test_result_value.append(Disease_diff_1)
        
    print("一階差分做格蘭傑")
    Medicine_diff_granger = grangercausalitytests(Medicine_Disease_diff_1[['Disease_Number','Medicine_Number']], maxlag=1)#一階插分格蘭傑
    Disease_diff_granger = grangercausalitytests(Medicine_Disease_diff_1[['Medicine_Number','Disease_Number']], maxlag=1)

    Medicine_diff_granger_value = Medicine_diff_granger[1]
    Medicine_diff_granger_value = Medicine_diff_granger_value[0]
    Medicine_diff_granger_value = Medicine_diff_granger_value['ssr_chi2test']
    Medicine_diff_granger_value = str(Medicine_diff_granger_value[1])
                
    Disease_diff_granger_value = Disease_diff_granger[1]
    Disease_diff_granger_value  = Disease_diff_granger_value [0]
    Disease_diff_granger_value  = Disease_diff_granger_value ['ssr_chi2test']
    Disease_diff_granger_value  = str(Disease_diff_granger_value [1])


    Test_result_value.append(Medicine_diff_granger_value)
    Test_result_value.append(Disease_diff_granger_value)
    
    print("二階差分")
    Medicine_Disease_diff_2 = Medicine_Disease_diff_1.diff(periods = 1)#二階插分將時間從不平穩到平穩
    Medicine_Disease_diff_2 = Medicine_Disease_diff_2.fillna(0)

    Medicine_diff_2 = unitroot_adf(Medicine_Disease_diff_2['Medicine_Number'])#二階插分檢驗平穩
    Disease_diff_2 = unitroot_adf(Medicine_Disease_diff_2['Disease_Number'])
    Medicine_diff_2 = Medicine_diff_2[1]
    Disease_diff_2 = Disease_diff_2[1]
    Test_result_value.append(Medicine_diff_2)
    Test_result_value.append(Disease_diff_2)
        
    print("二階差分做格蘭傑")
    Medicine_diff_granger_2 = grangercausalitytests(Medicine_Disease_diff_2[['Disease_Number','Medicine_Number']], maxlag=1)#二階插分格蘭傑
    Disease_diff_granger_2 = grangercausalitytests(Medicine_Disease_diff_2[['Medicine_Number','Disease_Number']], maxlag=1)

    Medicine_diff2_granger_value = Medicine_diff_granger_2[1]
    Medicine_diff2_granger_value = Medicine_diff2_granger_value[0]
    Medicine_diff2_granger_value = Medicine_diff2_granger_value['ssr_chi2test']
    Medicine_diff2_granger_value = str(Medicine_diff2_granger_value[1])

    Disease_diff2_granger_value = Disease_diff_granger_2[1]
    Disease_diff2_granger_value  = Disease_diff2_granger_value [0]
    Disease_diff2_granger_value  = Disease_diff2_granger_value ['ssr_chi2test']
    Disease_diff2_granger_value  = str(Disease_diff2_granger_value [1])
            
    Test_result_value.append(Medicine_diff2_granger_value)
    Test_result_value.append(Disease_diff2_granger_value)
    
    print("共整合檢驗")
    Medicine_Disease_coint = coint(df['Medicine_Number'],df['Disease_Number'])#協整檢驗
    coint_value = str(Medicine_Disease_coint[1])
    Test_result_value.append(coint_value)
    Test_result_value_1.append(Test_result_value)

Result_value = pd.DataFrame(Test_result_value_1)
Result_value = Result_value.rename(columns = {0:"icd9",1:"藥物時間平穩檢驗",2:"疾病時間平穩檢驗",3:"藥物格蘭傑檢驗",4:"疾病格蘭傑檢驗",5:"藥物一階差分P值",6:"疾病一階差分P值",7:"藥物一階差分蘭傑檢驗",8:"疾病一階差分蘭傑檢驗",9:"藥物二階差分P值",10:"疾病二階差分P值",11:"藥物二階差分蘭傑檢驗",12:"疾病二階差分蘭傑檢驗",13:"共整合檢定"})
Result_value.to_csv("C:/Users/USER/Desktop/25002_A10/25002_date_distrbuted_number/A10_granger_value(month).csv",encoding='UTF-8_sig',index=False)