# Data Mining Course Project

This project was performed on windows 10 operating system. Initially jupyter notebooks were used for the building of code and then it was converted to python script.

## Introduction 

Twitter is a microblogging platform which enables us to write our thoughts and express ourselves in few words. This data is public and available in the form of tweets and retweets. As twitter is a user-base that covers people from all the educational as well as geographical backgrounds, there are millions of threads of conversations on different topics like health, sports, technology, business and many more. This data can be thought of as a goldmine of information. But there is no use of it if we do not know how to mine the relevant data out of these conversations. One example can be online news media. Online news channels need to generate rich and timely information everyday which is possible through the twitter data. But, to find relevant information from the tweets and retweets will require large amount of efforts. There is a huge need to monitor and summarize this data. The concern is that the twitter data is a temporal data and thus the popular topics changes after a period of time. Thus we may find important topics which are popular for certain time intervals but not throughout the data set. We call here these popular topics as the frequent item sets which are locally frequent in the data set. Normally these locally frequent sets are periodic in nature. The aim of the project is to find these locally popular topics in the twitter data. It proposes a modification to Apriori algorithm to compute locally frequent sets.

## Directory Structure

### data

eval1.csv- Data for evaluation phase 1

eval2.csv- Data for evaluation phase 2

whole_data_processed- Whole twitter data after processing

partial_data_preprocessed- data with 50000 records preprocessed

covid19_tweets_without_preprocessing- raw dat 

### doc

Contains the project report

### src

Data Preprocessing.ipynb- jupyter notebook code for preprocessing

modified_apriori.ipynb-  jupyter notebook code for implementation

modified_apriori.py- python script for implementation

### outputs

contains outputs of various runs

whole_data_processed1, whole_data_processed2, whole_data_processed3, whole_data_processed4- outputs of runs made on whole_data_processed dataset

evaluation1_0,evaluation1_1, evaluation1_2, evaluation1_3,evaluation1_4- outputs of runs made on eval1 dataset

evaluation2_1, evaluation2_2, evaluation2_3,- outputs of runs made on eval2 dataset.

## How to run the code

Every time the implementation run is made, User is asked for an input for which dataset to run on:

`` Please enter number for which data to use: 1:twitter data, 2:Evaluation 1 data, 3:Evaluation 2 data, 4: twitter partial data``

The user needs to enter a digit between 1-4

1 - runs the implementation on the whole_data_processed

2 - eval1.csv

3 - eval2.csv

4 - partial_data_preprocessed.csv

After giving the input , press enter. The output of the code is then stored in the 'outputs' folder. the output file is named according to the respective inputs. 

1. whole_data_processed
2. evaluation1
3. evaluation2
4. partial_data_preprocessed

note: 1. It is preferable to run the script on eval1 or eval2 (2 or 3) first as it gives results quickly. The implementation on whole_data_processed takes a huge amount of time of around 2hrs. as the data set is very large.

2. After the first run if the user is trying to run the implementation on the same dataset then it is required to changes the name of the old file stored for that dataset. 



### Ways of running the implementation

2. Running python script (modified_apriori.py-)- Python script in the src folder can be executed using command prompt.

   note: The python script was tested using anaconda prompt

3. Running jupyter notebook file(modified_apriori.ipynb)- this file can be executed in jupyter notebook   

  