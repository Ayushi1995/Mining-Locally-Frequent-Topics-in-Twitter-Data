#!/usr/bin/env python
# coding: utf-8

# In[65]:


import numpy as np

import itertools
import collections
import collections.abc
import numbers
import typing
from abc import ABC, abstractmethod
import pandas as pd
import itertools
import re
import os
from datetime import datetime, timedelta 

from collections import defaultdict
from dataclasses import field, dataclass
from datetimerange import DateTimeRange
import os.path


# In[66]:


#Generating list of unique words
def unique_words(data):
    all_words=[]

    for column in data.columns[1:]:
        all_words.extend(data[column].unique().tolist())
    all_words=list(set(all_words))
    clean_words= [x for x in all_words if pd.notna(x)]
    #print(list(set(all_words)))
    return clean_words


# In[67]:


# Function foe generating L1
def level_one_frequent(data_map, local_support, minthd1, minthd2):
    #convert int to timedelta for comparision
    minthd1= timedelta(minthd1)
    minthd2= timedelta(minthd2)
    #Gen list of unique words item sets of size 1
    all_words=unique_words(data_map)
    
    n= len(all_words)
    tp= [[] for i in range(n)]
    supp=[[] for i in range(n)]
    #initialize all counters to zero
    
    last_seen=[0]*n
    first_seen=[0]*n
    icount=[0]*n
    ctcount=[0]*n
    ptcount=[0]*n
    # map of item to time instances
    L1={}
    supp1_map={}
    for index, row in data_map.iterrows():
        #print("row[0]",row[0])
        time_stamp=pd.to_datetime(row[0],dayfirst=True)
        transaction=list(row[1:])
        #if len(transaction)!=0:
        l=0
        #iterate over each word in the set of unique words
        for k, word in enumerate(all_words):
            #iterate through every transaction
            if word in transaction:
                #check last seen
                if(last_seen[k]==0):
                        last_seen[k]=first_seen[k]=time_stamp
                        icount[k]=ptcount[k]=ctcount[k]=1
                #If difference less than minthd1 increase the count
                elif(abs(time_stamp-last_seen[k])<minthd1):
                    last_seen[k]=time_stamp
                    icount[k]+=1
                    ctcount[k]+=1
                    ptcount[k]=ctcount[k]
#               #else check for minthd2 and support
                else:
                    if((abs(last_seen[k]-first_seen[k])>=minthd2) and ((icount[k]/ptcount[k]*100)>=local_support)):
#                         
                        tp[k].append([first_seen[k], last_seen[k]])
                        supp[k].append(["{:.2f}".format(icount[k]/ptcount[k]*100)])
                    #reset the count and times    
                    icount[k]=ptcount[k]=ctcount[k]=1
                    last_seen[k]=first_seen[k]=time_stamp

            else:
                #increment transaction count for the particular time interval
                ctcount[k]+=1
    #iterate through all the words to record time spans and supports
    for k in range(len(all_words)):
        if(last_seen[k]!=0 and first_seen[k]!=0):
            if((abs(last_seen[k]-first_seen[k])>=minthd2) and ((icount[k]/ptcount[k]*100)>=local_support)):
                tp[k].append([first_seen[k], last_seen[k]])
                supp[k].append(["{:.2f}".format(icount[k]/ptcount[k]*100)])
                
            if(len(tp[k]) !=0):
                L1[all_words[k]]=tp[k]
            if(len(supp[k])!=0):
                supp1_map[all_words[k]]=supp[k]
                
                
    return L1, supp1_map
            


# In[68]:


#Function for getting the intersection between 2 time stamps andtheir comparision with minthd2 
def valid_time_intersection(t1,t2,minthd2):
    minthd2= timedelta(minthd2)
    intersection_range=[]
    for datetm1 in t1:
        #print('datetm1',datetm1)
        for datetm2 in t2:
            #print('datetm2',datetm2)
            range1=DateTimeRange(datetm1[0],datetm1[1])
            range2=DateTimeRange(datetm2[0],datetm2[1])
            #if intersection value exist and it is >= minthd2 then only add to list
            if(range1.is_intersection(range2) and range1.intersection(range2).timedelta>=minthd2):
                time_range_list=[]
                #print('timedelta',range1.intersection(range2).timedelta)
                #find intersection
                time_range = range1.intersection(range2)
                #convert to string
                time_range.start_time_format = time_range.end_time_format= "%Y-%m-%d %H:%M:%S"
                time_range.end_time_format = time_range.end_time_format= "%Y-%m-%d %H:%M:%S"
                #convert back to the pd format
                start_time=pd.to_datetime(time_range.get_start_time_str())
                end_time=pd.to_datetime(time_range.get_end_time_str())
                # add to the list
                time_range_list=[start_time, end_time]    
                #print('time_range_list',time_range_list)
                #add to the list of all the possible intersections
                intersection_range.append(time_range_list)
                
    return intersection_range


# In[69]:


#function to generate all the possible itemsets of size 2 from the given list of itemsets
def join_step(itemsets: typing.List[tuple], length):
    retrn_list=[]
    all_elem=[]
    for item in itemsets:
        all_elem.append(item[0])
    #print(all_elem)
    for a, b in sorted(itertools.combinations(all_elem, 2)):
#         print((a,) + (b,))
        retrn_list.append((a,) + (b,))
        
    return retrn_list
            


# In[70]:



def time_info():
        return 0
#Pruning on the basis of time interval intersection. thus generating candidates of size 2
def prune_step(L1:dict, itemsets: typing.Iterable[tuple], possible_itemsets: typing.List[tuple], minthd2:int):
    # For faster lookups
    
    itemsets = set(itemsets)
    
    time_dict=defaultdict(time_info)
    for possible_itemset in possible_itemsets:
        #If time range for the item sets of length 2 is not valid then remove it from the dictionary
        time_dict[possible_itemset]=valid_time_intersection(L1[possible_itemset[0]],L1[possible_itemset[1]],minthd2)
        if len(time_dict[possible_itemset])==0:
            del time_dict[possible_itemset]
    return time_dict


# In[71]:


#function for joining and generating possible candidates
def apriori_gen(L1, itemsets, minthd2):
    possible_extensions = join_step(itemsets, 2)
    return prune_step(L1,itemsets, possible_extensions,minthd2)
    


# In[72]:



def level_two_frequent(Possible_itemsets, data_map, local_support, minthd1, minthd2):
    #convert number into timedelta
    minthd1= timedelta(minthd1)
    minthd2= timedelta(minthd2)
    
    n=len(Possible_itemsets)
    #initialize all the counts
    tp= [[] for i in range(n)]
    supp=[[] for i in range(n)]
    last_seen=[0]*n
    first_seen=[0]*n
    icount=[0]*n
    ctcount=[0]*n
    ptcount=[0]*n
    # map of item to time instances
    L2={}
    supp2_map={}
    for index, row in data_map.iterrows():
        #print(type(row))
        
        time_stamp=pd.to_datetime(row[0],dayfirst=True)
        transaction=list(row[1:])
        #for k, word in enumerate(all_words):
        for k, Possible_itemset in enumerate(Possible_itemsets):
            issubset = set.issubset
            if issubset(set(Possible_itemset), transaction):
                if(last_seen[k]==0):
                    last_seen[k]=first_seen[k]=time_stamp
                    icount[k]=ptcount[k]=ctcount[k]=1
                elif(abs(time_stamp-last_seen[k])<minthd1):
                    last_seen[k]=time_stamp
                    icount[k]+=1
                    ctcount[k]+=1
                    ptcount[k]=ctcount[k]
                else:
                    if((abs(last_seen[k]-first_seen[k])>=minthd2) and ((icount[k]/ptcount[k]*100)>=local_support)):
                        tp[k].append([first_seen[k], last_seen[k]])
                        supp[k].append(["{:.2f}".format(icount[k]/ptcount[k]*100)])
                        #tp.insert(k,[first_seen[k], last_seen[k]])
                    icount[k]=ptcount[k]=ctcount[k]=1
                    last_seen[k]=first_seen[k]=time_stamp
                        
            else:
                ctcount[k]+=1
                   
    for k in range(len(Possible_itemsets)):
        if(last_seen[k]!=0 and first_seen[k]!=0):
            if((abs(last_seen[k]-first_seen[k])>=minthd2) and ((icount[k]/ptcount[k]*100)>=local_support)):
                tp[k].append([first_seen[k], last_seen[k]])
                supp[k].append(["{:.2f}".format(icount[k]/ptcount[k]*100)])
            if(len(tp[k]) !=0):
                L2[Possible_itemsets[k]]=tp[k]
            if(len(supp[k])!=0):
                supp2_map[Possible_itemsets[k]]=supp[k]
    return L2, supp2_map
    
    


# In[73]:




def frequent_itemsets(data_map, local_support, minthd1, minthd2):
    itemsets=[]
    #construct and filter size 1 itemsets
    L1, supp1=level_one_frequent(data_map, local_support, minthd1, minthd2)
    for key, value in L1.items():
        single_key=[]
        single_key.append(key)
        itemsets.append(tuple(single_key))
    #construct next level candidate itemsets
    c_k_map = apriori_gen(L1, itemsets, minthd2)
    possible_itemsets=[key for key, value in c_k_map.items()]
    #filter size 2 itemsets
    L2, supp2=level_two_frequent(possible_itemsets, data_map, local_support, minthd1, minthd2)
    #supp1 and supp2 are the maps of itemset ti their respective supports
    return L1, supp1, L2, supp2



# In[74]:


if __name__ == "__main__":
    #Read and Store file
    my_path = os.path.abspath(os.path.dirname("__file__"))
    data_to_use = input("Please enter number for which data to use: 1:twitter data, 2:Evaluation 1 data, 3:Evaluation 2 data, 4: twitter partial data ")
    #Specify path for i/p data
    if data_to_use=='1':
        file_path = os.path.join(my_path, "../data/whole_data_processed.csv")
        output_path=os.path.join(my_path, "../outputs/whole_data_processed.csv")
        local_support=2
        minthd1=2
        minthd2=4
    elif data_to_use=='2':
        file_path = os.path.join(my_path, "../data/eval1.csv")
        output_path=os.path.join(my_path, "../outputs/evaluation1.csv")
        local_support=20
        minthd1=2
        minthd2=3
    elif data_to_use=='3':
        file_path = os.path.join(my_path, "../data/eval2.csv")
        output_path=os.path.join(my_path, "../outputs/evaluation2.csv")
        local_support=22
        minthd1=2
        minthd2=3
    elif data_to_use=='4':
        file_path = os.path.join(my_path, "../data/partial_data_preprocessed.csv")
        output_path=os.path.join(my_path, "../outputs/partial_data_preprocessed.csv")
        local_support=2
        minthd1=2
        minthd2=4
    else: print("number not valid, please re-run the script")
            
    # read file and print head
    data_map=pd.read_csv(file_path, encoding="ISO-8859-1")
    data_map.head()
    
    # Parameters to edit
#     local_support=22
#     minthd1=2
#     minthd2=4
    #------------------------------------------------
    #Running the algorithm
    L1, supp1, L2, supp2=frequent_itemsets(data_map, local_support, minthd1, minthd2)
    L1_set = list(L1.keys()) 
    L1_time = list(L1.values()) 
    L2_set= list(L2.keys())
    L2_time=list(L2.values())

    L1_df={'Items':L1_set, 'Time-interval':L1_time, 'Support in percent':list(supp1.values())}
    L2_df={'Items':L2_set, 'Time-interval':L2_time, 'Support in percent':list(supp2.values())}
    df = pd.DataFrame(L1_df)
    df=df.append(pd.DataFrame(L2_df))
    #print(df)
    df.to_csv (output_path, index = False, header=True)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




