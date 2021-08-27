import pandas as pd
import numpy as np
from pandas import read_csv
import matplotlib.pyplot as plt
import json
from graphics import *  
plt.close("all")

url="https://raw.githubusercontent.com/SilverWWW/SilverWWW-OR-Hospital-Payment-Records-2018/main/2018%20(ONLY)%20Hospital%20Payment%20Report%20data.csv"

names = ['Service category','Procedure','Statewide indicator','Hospital','Number of discharges 2018',\
'25th percentile 2018','Median 2018', '75th percentile 2018']

#df = pd.read_csv(url)


hospital_data_file = open('2018 Hospital Payment Report data.csv')
hospital_data_dictionary = {}
statewide_data_dictionary = {}
procedure_names = []
hospital_names = []
#Setting up data containers for information

for line in hospital_data_file:
    line = line.strip()
    line = line.split(',')
    if line[0] == "Service category": #skip over the first line
        pass
    else:
        if line[2] == '0': #for all non statewide values
            if line[1] not in hospital_data_dictionary.keys(): #adding a procedure to the data for the first time
                hospital_data_dictionary[line[1]] = [(line[3],line[4], line[5], line[6], line[7])] #stored in a dictionary
                                                                                                   #key = procedure name,
                                                                                                   #vallue = (hsp name, procedure freq, 25, median, 75)
                                                                                                
            else:
                temp_list = hospital_data_dictionary[line[1]] #temporary list of the procedure values
                temp_list.append((line[3],line[4], line[5], line[6], line[7])) #append the data for each hospital
                hospital_data_dictionary[line[1]] = temp_list #replace the original value with the updated list
        
        elif line[2] == '1': #adding all statewide procedure information to a single list of tuples, formated the same as above
            statewide_data_dictionary[line[1]] = [(line[3], line[4], line[5], line[6], line[7])]


        if line[1] not in procedure_names: #list of all procedure names
              procedure_names.append(line[1]) 

        if line[3] == "Statewide":
            pass
        elif line[3] not in hospital_names: #list of all hospital names
            hospital_names.append(line[3])

procedure_frequencies = []
top_ten_procedures = []

for procedure in procedure_names: #create a tuple of each procedure with their respective frequencies (statewide)
    procedure_frequencies.append((procedure, int(statewide_data_dictionary[procedure][0][1])))

procedure_frequencies.sort(reverse=True, key=lambda x:x[1]) #sort them based on frequencies from highest to lowest
for procedure in procedure_frequencies:
    if len(top_ten_procedures) <10: #add the procedures in diminishing order to a new list, stop at 10 added
        top_ten_procedures.append(procedure)


#print("The top 10 most performed procedures are "+str(top_ten_procedures))
#print('')

#purpose: to perform a detailed analysis on a given procedure, to find the standout values related to this procedure
#argument: takes a procedure string as input
#output: printed statements displaying the found information
def procedure_analysis(procedure):
    
    print("The median state price for the procedure ["+procedure+"] is $"+statewide_data_dictionary[procedure][0][3])
    print("")
    
    highest_hospital_median = 0 #tracking down the highest median price for a given procedure
    for hospital_procedure_info in hospital_data_dictionary[procedure]:
        if int(hospital_procedure_info[3]) > highest_hospital_median:
            highest_hospital_median = int(hospital_procedure_info[3]) #storing the greatest price
            hospital_name = hospital_procedure_info[0] #storing the hospital charging the greatest price
    print("The highest hospital price median for the procedure ["+procedure+"] is $"+str(highest_hospital_median))
    print("This hospital is "+hospital_name)
    print("") #printing the findings

    highest_hospital_75th = 0 #doing the exact same, but for the 75th percentile as opposed to the median
    for hospital_procedure_info in hospital_data_dictionary[procedure]:
        if int(hospital_procedure_info[4]) > highest_hospital_75th:
            highest_hospital_75th = int(hospital_procedure_info[4])
            hospital_name = hospital_procedure_info[0]
    print("The highest hospital 75h percentile price for the procedure ["+procedure+"] is $"+str(highest_hospital_75th))
    print("This hospital is "+hospital_name)
    print("") #printing the findings

    print("The ratio of the hospital with the highest median price to the median state price is "+str((highest_hospital_median/int(statewide_data_dictionary[procedure][0][3]))))
    print("")

    print("The ratio of the hospital with the highest 75th percentile price to the median state price is "+str((highest_hospital_75th/int(statewide_data_dictionary[procedure][0][3]))))
    print("")
    print("##################################################################################################")

#purpose: to conduct analysis, using the function above, on the most frequent procedures performed statewide
#argument: none
#output: 10 individual groups of statements on the most frequently performed procedures statewide
def top_ten_analysis():
   
    procedure_names_isolated = [] #isolating the names of the most performed procedures 
    for tuple in top_ten_procedures:
        procedure_names_isolated.append(tuple[0])

    for procedure in procedure_names_isolated:
        procedure_analysis(procedure) #loops through analysis and prints results

#top_ten_analysis()



hospital_procedures_info = {}

#purpose: normalize hospital median prices for every procedure, relative to eachother
#argument: takes a procedure string as input
#output: creates a dictionary with each hospital as a key, and their respective lists of normalized values
def next_step_analysis(procedure):
        
    counter = 0
    procedure_median_list = []
    for hospital_info in hospital_data_dictionary[procedure]:
        procedure_median_list.append(int(hospital_info[3])) #creating a list of medians for a selected procedure
        counter+=1

        if hospital_info[0] not in hospital_procedures_info.keys():
            hospital_procedures_info[hospital_info[0]] = [] #creating a dictionary where each hospital name is a key, empty values

    procedure_median_sum = 0
    for procedure_median in procedure_median_list:
        procedure_median_sum+=procedure_median
    procedure_median_mean = procedure_median_sum/counter #taking the average of a procedure's medians, a mediann mean


    squared_differences_list = []
    for procedure_median in procedure_median_list:
        squared_differences_list.append((procedure_median - procedure_median_mean)**2) #subtract procedure mean from median for each hospital,
                                                                                       #add the differences to a list

    squared_difference_sum = 0
    procedure_median_sd = 0
    for squared_difference in squared_differences_list:
        squared_difference_sum += squared_difference
        mean = squared_difference_sum/len(squared_differences_list)
        procedure_median_sd = mean**(1/2) #calculations to arrive at the standard deviation of the procedure's hospital medians

    normalized_list = []
    for hospital_info in hospital_data_dictionary[procedure]: #accessing list of tupled information for each hospital
        normalized_procedure_value = (int(hospital_info[3])-procedure_median_mean)/procedure_median_sd #now we take the normalized value
                                                                                                       #of each hospital's procedure median.
                                                                                                       #this means the average hospital normalized
                                                                                                       #value for any procedure will be 0.
                                                                                                       #a value such as 1.5 would indicate a higher
                                                                                                       #than average price relative to its alternatives.
        temp_list = hospital_procedures_info[hospital_info[0]] #going back to the dictionary we created before
        temp_list.append(normalized_procedure_value) #adding the normalized value to a list of normalized values of other procedures from the same hospital
        hospital_procedures_info[hospital_info[0]] = temp_list #setting the list back to the dictionary
        
        normalized_list.append(normalized_procedure_value) #creates a list allowing the viewing of the distribution of the normalized values for a procedure


final_hospital_data = []

#purpose:
#argument: none
#result:
def normalized_values_for_hospitals():

    for procedure in procedure_names:
        next_step_analysis(procedure) #create full lists of normalized procedures for every hospital in one dictionary
 
    for hospital in hospital_names:
        normalization_sum = 0
        normalization_list = hospital_procedures_info[hospital]
        for normalization in normalization_list:
            normalization_sum+= normalization
        normalization_mean = normalization_sum/len(normalization_list) #find the mean of all procedure normalizations for a hospital
        final_hospital_data.append((hospital, normalization_mean)) #create a final list of every hospital and its average procedure normalization value
        final_hospital_data.sort(reverse=True, key=lambda x:x[1]) #sort the list based on the values from largest to smallest, worst to best

    print(final_hospital_data)
    #print("The top 5 hospital charging the most on average for any given procedure are " +str(final_hospital_data[0:5]))




makeGraphicsWindow(800, 450)

def startWorld(world):
    normalized_values_for_hospitals()

def updateWorld(world):
    pass

def drawWorld(world):
    
    counter=1
    for mean_normalized_value in final_hospital_data[0:5]:
        
        fillRectangle(60*counter-30, 225-100*mean_normalized_value[1], 50, 100*mean_normalized_value[1], "red")

        drawString(str(counter)+": ", 30, 240+30*counter, 30, "black")
        drawString(mean_normalized_value[0], 50, 243+30*counter, 23, "black")         
        
        
        
        counter+=1
    



    counter2=1
    for mean_normalized_value in final_hospital_data[-6:-1]:

        fillRectangle(60*counter2+420, 225, 50, -100*mean_normalized_value[1], "blue")

        drawString(str(counter2)+": ", 480, 15+30*counter2, 30, "black")
        drawString(mean_normalized_value[0], 500, 198-30*counter2, 23, "black")


        counter2+=1



    fillRectangle(398, 0, 4, 450, "black")
    drawString("Average hospital median procedure cost", 105, 230, 23, "green", italic=True)
    drawString("+1.65", 30, 40, 25, "red")
    drawString("-1.01", 725, 330, 25, "blue")
    drawString("Most Expensive Hospitals", 20, 420, 40, "red")
    drawString("Least Expensive Hospitals", 420, 5, 40, "blue")
    fillPolygon([(320,145),(400, 225),(320,225)],"red")
    fillPolygon([(400,225),(480,225),(480,283)],"blue")

    fillRectangle(0, 224, 800, 2, "green")


runGraphics(startWorld, updateWorld, drawWorld)













print("")
print("")
print("")



"""

The following is old code that is redundant in hindsight, but nonetheless useful.

#purpose: find the standard deviation for the median prices of a procedure
#argument: takes a procedure string as input
#output: a statement displaying the inputted procedure's standard deviation
def hospital_procedure_comparison(procedure):
    
    hospital_median_sum = 0
    hospital_median_list = []

    for hospital_procedure_info in hospital_data_dictionary[procedure]: #accessing list of tupled information for each procedure
        hospital_median_sum += int(hospital_procedure_info[3]) #sum of procedure median prices from all hospitals
        hospital_median_list.append(int(hospital_procedure_info[3])) #list of all median procedure prices from all hospitals
    hospital_mean = hospital_median_sum/len(hospital_median_list) #taking the average median price of a procedure from every hospital

    squared_differences_list = [] #begin finding the standard deviation of a procedure with the prices from every hospital
    for hospital_median in hospital_median_list:
        squared_differences_list.append(hospital_median - hospital_mean)**2 #subtract procedure mean from median for each hospital,
                                                                            #add the differences to a list

    squared_difference_sum = 0
    hosp_sd = 0
    for squared_difference in squared_differences_list:
        squared_difference_sum += squared_difference
        mean = squared_difference_sum/len(squared_differences_list) #take the sum of these differences,
        hosp_sd = mean**(1/2) #then take the sum's square root to find the standard deviation of prices for any given procedure

    print("The standard deviation in prices for the procedure "+str(procedure)+" is "+str(hosp_sd))




"""