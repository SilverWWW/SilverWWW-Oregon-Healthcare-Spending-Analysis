import pandas as pd
import numpy as np
from pandas import read_csv
import matplotlib.pyplot as plt
import json
plt.close("all")

url="https://raw.githubusercontent.com/SilverWWW/SilverWWW-OR-Hospital-Payment-Records-2018/main/2018%20(ONLY)%20Hospital%20Payment%20Report%20data.csv"

names = ['Service category','Procedure','Statewide indicator','Hospital','Number of discharges 2018',\
'25th percentile 2018','Median 2018', '75th percentile 2018']

#df = pd.read_csv(url)


hospital_data_file = open('2018 Hospital Payment Report data.csv')
hospital_data_dictionary = {}
statewide_data_dictionary = {}
procedure_names = []

for line in hospital_data_file:
    line = line.strip()
    line = line.split(',')
    if line[0] == "Service category":
        pass
    else:
        if line[2] == '0':
            if line[1] not in hospital_data_dictionary.keys():
                hospital_data_dictionary[line[1]] = [(line[3],line[4], line[5], line[6], line[7])]
            else:
                temp_list = hospital_data_dictionary[line[1]]
                temp_list.append((line[3],line[4], line[5], line[6], line[7]))
                hospital_data_dictionary[line[1]] = temp_list
        
        elif line[2] == '1':
            statewide_data_dictionary[line[1]] = [(line[3], line[4], line[5], line[6], line[7])]


        if line[1] not in procedure_names:
              procedure_names.append(line[1])

procedure_frequencies = []
top_ten_procedures = []

for procedure in procedure_names:
    procedure_frequencies.append((procedure, int(statewide_data_dictionary[procedure][0][1])))

procedure_frequencies.sort(reverse=True, key=lambda x:x[1])
for procedure in procedure_frequencies:
    if len(top_ten_procedures) <10:
        top_ten_procedures.append(procedure)


#print("The top 10 most performed procedures are "+str(top_ten_procedures))
#print('')


def procedure_analysis(procedure):
    
    print("The median state price for the procedure ["+procedure+"] is $"+statewide_data_dictionary[procedure][0][3])
    print("")
    
    highest_hospital_median = 0
    for hospital_procedure_info in hospital_data_dictionary[procedure]:
        if int(hospital_procedure_info[3]) > highest_hospital_median:
            highest_hospital_median = int(hospital_procedure_info[3])
            hospital_name = hospital_procedure_info[0]
    print("The highest hospital price median for the procedure ["+procedure+"] is $"+str(highest_hospital_median))
    print("This hospital is "+hospital_name)
    print("")

    highest_hospital_75th = 0
    for hospital_procedure_info in hospital_data_dictionary[procedure]:
        if int(hospital_procedure_info[4]) > highest_hospital_75th:
            highest_hospital_75th = int(hospital_procedure_info[4])
            hospital_name = hospital_procedure_info[0]
    print("The highest hospital 75h percentile price for the procedure ["+procedure+"] is $"+str(highest_hospital_75th))
    print("This hospital is "+hospital_name)
    print("")

    print("The ratio of the hospital with the highest median price to the median state price is "+str((highest_hospital_median/int(statewide_data_dictionary[procedure][0][3]))))
    print("")

    print("The ratio of the hospital with the highest 75th percentile price to the median state price is "+str((highest_hospital_75th/int(statewide_data_dictionary[procedure][0][3]))))
    print("")
    print("##################################################################################################")

def top_ten_analysis():
   
    procedure_names_isolated = []
    for tuple in top_ten_procedures:
        procedure_names_isolated.append(tuple[0])

    for procedure in procedure_names_isolated:
        procedure_analysis(procedure)

#top_ten_analysis()

    





            
















"""
#print(df['Service category'])
bone_study_medians_2018 = {}
hospital_list_in_order = []
bone_study_median_list_in_order =[]


count = 0
for procedure in df['Procedure']:
    if procedure == "Bone study":
        bone_study_medians_2018[df["Hospital"][count]]=df['Median 2018'][count]
        hospital_list_in_order.append(df["Hospital"][count])
        bone_study_median_list_in_order.append(df['Median 2018'][count])
        count+=1

test_series = pd.Series(bone_study_medians_2018)

d = {
    "Hospital": pd.Series([hospital_list_in_order[1],hospital_list_in_order[2],hospital_list_in_order[3]]),
    "Median 2018": pd.Series([bone_study_median_list_in_order[1],bone_study_median_list_in_order[2],bone_study_median_list_in_order[3]]),
}

bsm2018_df = pd.DataFrame(d)

print(test_series)
"""