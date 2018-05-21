
# coding: utf-8

# In[ ]:

# The minimum number of items that could make up to target price is one and the maximum number is all the items. My ideas was to 
#generate combinations of items in the file  from one to total number of items .


# In[204]:

#Author: Yaswanth Reddy Vayalpati
#importing all necessary packages
import csv
import itertools
import re
import os
import pandas as pd
import sys


# In[205]:

#This function takes a number and returns number of digits that are present after the decimal point.
#This count was used to round the sum, when the sum of prices of the items were calculated.
def num_after_point(number):
    number_string = str(number)
    if not '.' in number_string:
        return 0
    return len(number_string) - number_string.index('.') - 1


# In[206]:

#This function takes a dictionary  and a integer value as paramters, generates combinations for dictionary elements with 
#length of each combination equal to the  integer value we pass to the function and adds them to a list and returns it.
def generateCombinations(menu_items,length):
    #Code to generate combinatios with each of length equal to the integer
    result_list = list(map(dict, itertools.combinations(menu_items.items(), length)))
    return result_list


# In[207]:

#This function takes two parameters, one is the dictionary of items and the other is length of combinations 
# If the length passed to this function is greater than the total items then the call returns.
#Else this function calls generateCombinations function with the items dictionary and the length and adds the received combinatios
#to a total combinations list.
#This function then calls itself recursively with length incremented by 1.
#This function returns a list with all possible combinations
def getTotalCombinations(items,start_length):
    if(start_length>(len(items.values()))):
        return
    else:
        current_length_combinations=generateCombinations(items,start_length)
        all_combinations.append(current_length_combinations)
        getTotalCombinations(items,start_length+1)
    return all_combinations


# In[208]:

#This functions takes a file name as a parameter and checks of the file exists or not
# Then it checks if the file is empty or not
#This function then reads the file and puts it into a pandas dataframe
#This function separates target price and puts all items in a dictionary.
#This function also converts numbers in string formats to floats
#This function then calls "getTotalCombinations" function with items dictionary and length as 1.
def checkForCombinations(fileName):
    #Checking if file exists or not
    if os.path.exists(fileName):
        #Checking if file sis empty or not
        if(os.stat(fileName).st_size != 0):
            #Blanks dictionary for items
            items_dictionary={}
            count=0
            target_price=""
            #reading CSV file and putting it in pandas dataframe
            dataf=pd.read_csv(fileName,header=None)
            #Removing blank rows
            dataf=dataf.dropna()
            dataf[0][0]=dataf[0][0].lower()
            #Checking if the first row's first column has target price string .This condition is case insensitive
            if(dataf[0][0]=="target price"):
                #iterating through each row
                for row in dataf.itertuples():
                    try:
                        #Converting numbers in string format to float
                        value=re.search("[-+]?\d*\.\d+|\d+", row[2]).group()
                        value=float(value)
                    except:
                        print("Cannot convert one of the Values as there is not number")
                    if(count==0):
                        target_price=(value)
                    else:
                        #building items dictionary
                        items_dictionary[row[1]]=(value)
                    count=count+1
                rounding_digits=num_after_point(target_price)

                #This line calls the "getTotalCombinations" function which inturn makes recursive calls and also to "generateCombinations"
                all_combinations_list=getTotalCombinations(items_dictionary,1)

                #Count varaiable to count number of combinations that pass the criteria
                combination_count=0

                #This nested for loop separates combinations of different lengths and inturn separates each combination
                for each_combination_list in all_combinations_list:
                    for each_combination in each_combination_list:
                        #Checking if the sum of prices of the combination is equal to target
                        if(round(sum(each_combination.values()),rounding_digits)==target_price):
                            print("The sum of following combination is equal to target")
                            #Printing combinations that satisfy the condition
                            for keys in each_combination.keys():
                                print(keys,' ',each_combination[keys])
                            combination_count=combination_count+1
                            print()

                #If count is zero printing that no combinations matche the criteria
                if(combination_count==0):
                    print("There is no combination of dishes that is equal to the target price")
            else:
                print("First column of first row should be 'target price'. Case of the string doesn't matter")
        else:
            print("File is Empty.")
    else:
        print("File doesn't exist. Please provide file name and its path")


# In[210]:

#If there is only one command line argument is provided or not
if(len(sys.argv)==2):
    #List to store all combinations
    all_combinations=[]
    # function call to open the file and generate combinations
    checkForCombinations(sys.argv[1])
#Condition to check if no arguments were provided
if(len(sys.argv)==1):
    print("Please provide file name as command line parameter")
#Condition to check if more than one command line argument is provided
if(len(sys.argv)>2):
    print("Please provide only one file name as command line parameter")


# In[ ]:



