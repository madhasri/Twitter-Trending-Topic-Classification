import csv
import pandas
import openpyxl
from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier




my_list = []
my_dict = {}
tech_list = []
sports_list = []
my_test_list = []
d = [[] for x in xrange(0,6)]
filelist = ['tech_raw.txt' , 'sports_raw.txt','fnl_raw.txt','business_raw.txt','politics_raw.txt','ent_raw.txt']
filelist1 = ['tech_raw_test.txt' , 'sports_raw_test.txt','fnl_raw_test.txt','business_raw_test.txt','politics_raw_test.txt','ent_raw_test.txt']
label = ['tech' , 'sports','fnl','business','politics','entertainment']
j=0

for k in range(0,len(filelist)):
 my_list= open(filelist[k], 'r').read().split('\n')
 my_list = list(set(my_list))
 for i in range(0,len(my_list)):
  my_dict["category"] = label[j]
  my_dict["text"] = my_list[i]
  d[j].append(my_dict.copy()) 
 j=j+1


'''
print d[0]
print d[1]
print d[2]
print d[3]
print d[4]
'''
finald = d[0] + d[1] + d[2] + d[3] + d[4] + d[5]

tweetTrainer = Trainer(tokenizer)

# Train the system passing each text one by one to the trainer module.

'''
{'text': 'not to eat too much is not enough to lose weight', 'category': 'health'},
{'text': 'Russia is trying to invade Ukraine', 'category': 'politics'},
{'text': 'do not neglect exercise', 'category': 'health'},
{'text': 'Syria is the main issue, Obama says', 'category': 'politics'},
{'text': 'eat to lose weight', 'category': 'health'},
{'text': 'you should not eat much', 'category': 'health'}
'''

for tweet in finald:
    tweetTrainer.train(tweet['text'], tweet['category'])

# When you have sufficient trained data, you are almost done and can start to use a classifier.
truth_list = []
pred_list = []
tweetClassifier = Classifier(tweetTrainer.data, tokenizer)
test_tweets = []

# Try to classifiy tweet whose category is unknown yet using the trained classifier.
unknownInstance = ""
#print accuracy on each category

k=0

for j in range(0,len(filelist1)):
 my_test_list= open(filelist1[j], 'r').read().split('\n')
 my_test_list = list(set(my_test_list))
 l = len(my_test_list)
 count = 0
 #counter = [0,0,0,0,0]
 for i in range(0,l):
  truth_list.append(label[k])
    
  classification = tweetClassifier.classify(my_test_list[i])
  pred_list.append(classification[0][0])
  if(classification[0][0] == label[k]):
   count = count + 1
  

   
 print count
 print l
 print label[k] 
 print ":" 
 print float((count*100)/l)
 k=k+1 
 #print pred_list
 
#classification = tweetClassifier.classify(unknownInstance)
# the classification variable holds the possible categories sorted by their probablity value
#print classification


df = pandas.DataFrame({'predicted' : pred_list})
df['truth'] = truth_list
df.to_excel('firsttry.xlsx' , sheet_name = 'sheet1', index=False)
