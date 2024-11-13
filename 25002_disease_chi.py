# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:43:41 2023

@author: USER
"""

import csv
import numpy as np
from scipy.stats import chi2_contingency
import time


start = time.process_time()
dict_first_time = {}
dict_icd9 = {}
dict_id = {}
with open('D:/Landseed_medicine/landseed_first_time_icd9.csv') as file_first_time:
     filereader_first_time  = csv.reader(file_first_time)
     for row in filereader_first_time:
         dict_first_time.update({(row[0],row[1]):0})
with open('D:/Landseed_medicine/landseed_list_icd9.csv') as file_icd9:
    filereader_icd9 = csv.reader(file_icd9)
    for row1 in filereader_icd9:
        dict_icd9.update({(row1[0]):0})
with open("D:/Landseed_medicine/landseed_list_id.csv") as file_id:
    filereader_id = csv.reader(file_id)
    for row2 in filereader_id:
        dict_id.update({(row2[0]):0})
       
disease_1 =['25002']
for d in disease_1:
    fh_w = open('C:/Users/USER/Desktop/25002_A10/25002_chi/'+d+'_chi.csv','w')
    fh =  open('C:/Users/USER/Desktop/25002_A10/sick_list/'+d+'_sick_list.csv','w')
    
    disease = []

    print(d)
    disease.append(d)
    for key_icd9 in dict_icd9:
        values_a = 0
        values_b = 0
        values_c = 0
        values_d = 0
        for key_id in dict_id:
            patient_362  =(key_id,d)
            want_to_find = (key_id,key_icd9)
            if patient_362 in dict_first_time:
                if want_to_find in dict_first_time:
                    values_a +=1
                else:
                    values_c +=1
            else:
                if want_to_find in dict_first_time:
                    values_b +=1
                else:
                    values_d +=1

        if values_a > 0 and values_b > 0 and values_c > 0 and values_d > 0:
            out_str = '{},{},{},{}'.format(values_a,values_b,values_c,values_d)
            out_list = out_str.split(',')
            a = np.array(out_list ,dtype='int64')
            obs = a.reshape((2,2))
            chi2, p, dof, expected = chi2_contingency(obs)
            OR_value = (values_a*values_d)/(values_b*values_c)
            print('{},{},{},{},{},{},{},{}'.format(key_icd9,values_a,values_b,values_c,values_d,chi2,p,OR_value))
            out = '{}'.format(key_icd9)
            out_str1 = '{},{},{},{},{},{},{},{}'.format(key_icd9,values_a,values_b,values_c,values_d,chi2,p,OR_value)
            disease.append(key_icd9)
            fh_w.write(out_str1 +'\n')
            fh.write(out+'\n')
    fh_w.close()
    fh.close()
end = time.process_time()
print("執行時間：  "+ str(int(end - start)/60)+"分")
