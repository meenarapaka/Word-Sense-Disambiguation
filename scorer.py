
#Team: Meena Rapaka, K.Siva Naga Lakshmi, Ying ke
#Assignment 4: Word Sense Disambiguation, file: scorer.py

#The output of decision-list.py file(my-line-answers.txt) is compared with the golden standard key (line-answers.txt) which is #provided, to calulate the accuracy and provide
#confusion matrix.

##The program should run on command prompt/ terminal, then specify the path of the python file.

#python scorer.py my-line-answers.txt line-answers.txt > wsdreport.txt

#once we execute the above command,a text file is generated as" wsdreport.txt" which comprises the results of comparisions of #my-line-answers.txt with line-answers.txt which is resulted as the accuracy.
#Confusion Matrix is also computed for the above listed comparisions.

#Algorithm
#1: Input is passed as sys arguments which are decision-list output file(my-line-answers.txt) and test key(line-answers.txt)
#2: Read the output file to create a dictionary to separate line and sense id 
#3: We are creating a new list to match the key and value pairs
#4: Match corresponding pairs from the model output to the test key and increment a counter each time when there is a match
#5: Find the accuracy of the model by dividing based on length as defined in the formula
#6: Find the confusion matrix by comparing output values with actual key values
#7: Output is stored into wsdreport.txt
#END




import sys
import nltk
import pandas as pd
import scipy
from nltk.metrics import ConfusionMatrix

def main():

    output_file = sys.argv[1] #passing my-line-answers.txt
    key_file = sys.argv[2]    #passing line-answers.txt
    
    with open(output_file) as file: #read my-line-answers.txt
        f1 = [line.rstrip('\n') for line in file] #each line of file is converted into each element of list
        var1= [i.split(':"', 1) for i in f1] #each line is split based on colon and quotes
        predicted = {} #declaring dictionary

    for a in range (1,len(var1)): #dictionary is created is passed instance id as key and sense id as value
        key=var1[a][0]
        value=var1[a][1]
        predicted[key]=value
   #Assuming a list and then using for loop reading the values from predicted and then appending them in the new list which is predicted_list.#
    predicted_list=[]                   
    for v in predicted:
        predicted_list.append(predicted[v])
        
    with open(key_file) as myf1: #read line-answers.txt 
        f2 = [line.rstrip('\n') for line in myf1] #each line of f1 is converted into each element of list
        var2= [i.split(':"', 1) for i in f2] #each line is split based on colon and quotes
        observed = {} #declaring dictionary

    for a in range (1,len(var2)): # every value from key and value are read
        key=var2[a][0]            #for every line in sentence, first part is considered as key
        value=var2[a][1]          #second part is considered as sentence
        observed[key]=value
    #Assuming a list and then using for loop reading the values from observed. and then appending them in the new list which is observed_list.# 
    observed_list=[]
    for v in observed:
        observed_list.append(observed[v])

    cm=ConfusionMatrix(observed_list,predicted_list) #calculating the consfusion matrix
    x=0
    for i in range(len(predicted_list)):
        if predicted_list[i] == observed_list[i]:  #comparing both the list values and if it is equal x gets incremented.
            x += 1
    accuracy = (x/len(predicted_list)*100) #calculating the accuracy

	#Accuracy and confusion matrix is stored in output file viz wsdreport.txt
    print('Accuracy of the classifier is:',accuracy,'\n\n''Confusion Matrix: ',str(cm),)
if __name__ == '__main__':
    main()
