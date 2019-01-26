
# coding: utf-8

# In[11]:


#Team: Meena Rapaka, K.Siva Naga Lakshmi, Ying Ke
#Assignment 4: Word Sense disambiguation, file: decision-list.py

#1.Introduction:
#Word Sense Disambiguation (WSD):This program helps us identify which sense of a word is used in a sentence when a word 
#has multiple meanings. WSD is an open problem of natural language processing and ontology.
#The main challenge in this program is to create a classifier which identifies the sense of the words (which can be used for
#multiple meanings) based on the input file. The input files line-train.xml(comprises examples of word line used in sense 
#of phone line and product line) and line-test.xml(comprises sentences that uses word line without any sense being indicated)
#and generates output file which will contain senses added to text file.
#For example,the sense of the word "sales" in phone sense is different from "sales" in product sense.

#2.Example input/output:
#The program should run on command prompt/ terminal, then specify the path of the python file
#python decision-list.py line-train.xml line-test.xml my-decision-list.txt > my-line-answers.txt
#all the files should be present in the same folder
#after running the above code, an output file my-line-answers.txt is created which has the output
#sample output would be as below:
#<answer instance="line-n.w8_059:8174:" senseid="phone"/>
#<answer instance="line-n.w7_098:12684:" senseid="phone"/>
#<answer instance="line-n.w8_106:13309:" senseid="product"/>

#3.Algorithm 
#1.Create a attribute list by identifying patterns from line-train.xml.And then associate attributes with sense
#2.Read the XML file into training argument
#3.Read the XML file based on the tag instance and read the context
#4.the context in xml file is separated based on tag sense
#5.Probability is calculated for each attribute in the corpus
#6.Sort the attributes accordingly based on their probability scores and a decision list is created
#7.Read the XML file into testing argument
#8.Read the XML file based on the tag instance and read the context
#9.Perform search on a particular attribute in the context
#10.If particular attribute is matched attribute list which is defined earlier,then assign the associated 
#sense to that particular context
#11.If no match is found,assign the default sense i.e., Phone
#12.The output is printed with the same standard as gold standard file.
#END

#my-line-answers.txt and my-decision-list.txt - the output files are saved in the same folder as the input files.
#To calculate accuracy and confusion matrix, run the scorer.py accordingly.



import re
import sys
from bs4 import BeautifulSoup
import math
#input files
TRAIN_XML = sys.argv[1] 
TEST_XML = sys.argv[2]
OUTPUT = sys.argv[3]
#TRAIN_XML = 'C:\\Users\\mynam\\Desktop\\PA4_Solution\\line-train.xml'
#TEST_XML = 'C:\\Users\\mynam\\Desktop\\PA4_Solution\\line-test.xml'
#OUTPUT = 'C:\\Users\\mynam\\Desktop\\PA4_Solution\\mydecision-list.txt'
#feature set is defined based on YarowskyDecision-List-1994.pdf paper
#Based on line-train.xml provided, we defined the below feature sets for product and phone sense
#for phone sense,we defined,vote_feature,growth_feature,computer_feature,telephone_feature,voice_feature,service_feature
#for product sense,we defined,sales_feature,dealers_feature,analysts_feature,network_feature,price_feature,sale_feature,market_feature

def feature_set():
  
    def vote_feature(line):
        return (re.search(r'vote', line), 'phone')
    yield vote_feature
    
    def growth_feature(line):
        return (re.search(r'growth', line), 'phone')
    yield growth_feature
    
    def sales_feature(line):
        return (re.search(r'sales',line),'product')
    yield sales_feature
    
    def computer_feature(line):
        return (re.search(r'computer',line),'phone')
    yield computer_feature
    
    def dealers_feature(line):
        return (re.search(r'dealers', line), 'product')
    yield dealers_feature

    def analysts_feature(line):
        return ('analyst' in line, 'product')
    yield analysts_feature
    
    def network_feature(line):
        return (re.search(r'network', line), 'product')
    yield network_feature

    def price_feature(line):
        return (re.search(r'price ', line), 'product')
    yield price_feature
    
    def telephone_feature(line):
        return ('telephone' in line, 'phone')
    yield telephone_feature

    def sale_feature(line):
        return (re.search(r'sale ', line), 'product')
    yield sale_feature

    def voice_feature(line):
        return ('voice' in line, 'phone')
    yield voice_feature

    def market_feature(line):
        return (re.search(r'market', line), 'product')
    yield market_feature

    def service_feature(line):
        return (re.search(r'service', line), 'phone')
    yield service_feature
    
featurelist = [f for f in feature_set()]

if __name__ == '__main__':  
    f=open(TRAIN_XML) #Input training file is open and read.
    data=f.read()
     
    parser = BeautifulSoup(data, 'xml') #we are using beautiful soup function for the xml format and passed into parser variable.
    
    textsense1 = [] 
    textsense2 = [] 
   
    for instance in parser.find_all('instance'):#parser function will find all the instances and if the sense id is phone and 
        #then it will append all the values in the textsense1.
        if instance.answer['senseid'] == 'phone':
            for tag in instance.find_all('s'): 
                string = tag.string
                textsense1.append(string)
        else:#if the sense id is other than phone which is product it will append the values in the textsense2 list.
            for tag in instance.find_all('s'):
                string = tag.string
                textsense2.append(string)
                
    #textsense_1, textsense_2 = Clean_text(textsense_1,textsense_2)

    def probability(attribute): #defining the probability of the attributes.
        count1 = 0 
        count2 = 0 
#Here we are considering sense and other text as sense1 input.
        sense_text = textsense1 
        other_text = textsense1
#if sense is compared with the product the sensetext will be equal to the sense2 and the other text will remain same as sense1.
        sense = attribute('')[1] 
        if sense == 'product':
            sense_text = textsense2
            other_text = textsense1
           # print(sense_text[:5])
          #  print(other_text[:5])
#for every line in the sense text if the value is none, the count1 is incremented..
        for line in sense_text:
            if line is not None and attribute(line)[0]:
                count1 += 1
#for every line in the other text, if the value is not none count2 is incremented.
        for line in other_text:
            if line is not None and attribute(line)[0]:
                count2 += 1
        total_count = count1 + count2#total count is calculated and then probability is also calculated with respect to count1
        #count2
        prob1 = count1 / total_count  
        prob2 = count2 / total_count 
        
        try:
            ratio = math.log10(prob1 / prob2)#ratio of the probability using the log function.
        except ZeroDivisionError:#if the ratio is 0, it will replace with 1.
            ratio = 1
        
  #the ratio values are written in the output file which is mydecision-list.txt.      
        with open(OUTPUT, 'a+') as output:
            output.write(f'{attribute.__name__}\t{ratio}\t{sense}\n')

        return ratio

    featurelist.sort(key=probability)

    phone = len(parser.find_all(senseid="phone")) #counts the numbers of times product is identified as phone 
    product = len(parser.find_all(senseid="product")) #counts the number of times product is identified as product.
    default = 'phone' #if phone > product else 'product'
   # Here the test file is opened and then read .
    y=open(TEST_XML)
    data=y.read()
    parser = BeautifulSoup(data, 'xml')#we are using beautiful soup function for the xml format and passed into parser variable.
  #Senses are identified and the tags are added accordingly.      
    for instance in parser.find_all('instance'):
        context = tuple(
                tag.string for tag in instance.find_all('s')
                if tag.string is not None
                )

        sense = None
        for line in context:#if attributes are matched with the feature list, sense of the test result is returned.
            for attribute in featurelist:
                test_result = attribute(line)
                #print(test_result[:5])
                if test_result[0]:
                    sense = test_result[1]
                    #print(sense)
                    break
        if sense is None:#if the sense is none it automatically considers the default sense which is phone.
            sense = default
            #print(sense)
        #prints the output in the format shown in the sample output.
        id_num = instance['id']
        print(f'<answer instance="{id_num}" senseid="{sense}"/>')

        #with open(OUTPUT_ANSWERS, 'a+') as output_check:
             #output_check.write(f'<answer instance="{id_num}" senseid="{sense}"/>\n')
            
            
        


# In[ ]:




