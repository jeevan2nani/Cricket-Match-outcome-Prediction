import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB

def execute() :

	matches=pd.read_csv('matches.csv')

	matches['winner'].fillna('Draw', inplace=True)

	matches.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
		         'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
		         'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors','Gujarat Lions','Rising Pune Supergiant','Delhi Capitals']
		        ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','GL','RPS','DD'],inplace=True)

	encode = {'team1': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'DD':7,'GL':8,'KXIP':9,'SRH':10,'RPS':11,'KTK':12,'PW':13,'GL':14,'RPS':15},
		  'team2': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'DD':7,'GL':8,'KXIP':9,'SRH':10,'RPS':11,'KTK':12,'PW':13,'GL':14,'RPS':15},
		  'toss_winner': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'DD':7,'GL':8,'KXIP':9,'SRH':10,'RPS':11,'KTK':12,'PW':13,'GL':14,'RPS':15},
		  'winner': {'MI':1,'KKR':2,'RCB':3,'DC':4,'CSK':5,'RR':6,'DD':7,'GL':8,'KXIP':9,'SRH':10,'RPS':11,'KTK':12,'PW':13,'GL':14,'RPS':15,'Draw':16}}

	matches.replace(encode, inplace=True)

	matches['city'].fillna('Dubai',inplace=True)

	xx=matches.groupby(["toss_winner"]).size()

	yy=matches.groupby(["winner"]).size()

	dicVal = encode['winner']

	matches = matches[['team1','team2','city','toss_decision','toss_winner','venue','winner']]

	df = pd.DataFrame(matches)

	cat_list=df["city"]

	encoded_data, mapping_index = pd.Series(cat_list).factorize()

	cat_list1=df["venue"]

	encoded_data1, mapping_index1 = pd.Series(cat_list1).factorize()

	cat_list2=df["toss_decision"]

	encoded_data2, mapping_index2 = pd.Series(cat_list2).factorize()

	temp1=df['toss_winner'].value_counts(sort=True)

	temp2=df['winner'].value_counts(sort=True)


	var_mod = ['city','toss_decision','venue']

	le = LabelEncoder()

	for i in var_mod:

	    df[i] = le.fit_transform(df[i])

	def classification_model(model, data, predictors, outcome) :
	      model.fit(data[predictors],data[outcome].values.ravel())
	      predictions = model.predict(data[predictors])
	      #print(predictions)
	      accuracy = metrics.accuracy_score(predictions,data[outcome])
	      return accuracy;
	      #print('Accuracy : %s' % '{0:.3%}'.format(accuracy))


	#Training the Dataset

	model = [0]*5

	#logistic Regression
	outcome_var=['winner']
	predictor_var = ['team1', 'team2', 'venue', 'toss_winner','city','toss_decision']
	model[0] =LogisticRegression()
	accuracy1= classification_model(model[0], df,predictor_var,outcome_var)

	#Gaussian NAive bayes algorithm
	outcome_var=['winner']
	predictor_var = ['team1', 'team2', 'venue', 'toss_winner','city','toss_decision']
	model[1] = GaussianNB()
	accuracy2=classification_model(model[1], df,predictor_var,outcome_var)

	#applying knn algorithm
	from sklearn.neighbors import KNeighborsClassifier
	model[2] = KNeighborsClassifier(n_neighbors=3)
	accuracy3=classification_model(model[2], df,predictor_var,outcome_var)


	#Decision tree algorithm
	from sklearn import tree
	model[3] = tree.DecisionTreeClassifier(criterion='gini')
	outcome_var=['winner']
	predictor_var = ['team1', 'team2', 'venue', 'toss_winner','city','toss_decision']
	accuracy4=classification_model(model[3], df,predictor_var,outcome_var)

	#Random Forest
	model[4] = RandomForestClassifier(n_estimators=100)

	outcome_var = ['winner']

	predictor_var = ['team1', 'team2', 'venue', 'toss_winner','city','toss_decision']

	accuracy5=classification_model(model[4], df,predictor_var,outcome_var)

	accuracy = np.array([accuracy1,accuracy2,accuracy3,accuracy4,accuracy5])


	#to find Most accurate Algorithm

	greatest=0
	temp=0
	for i in range(5):
		if(accuracy[i] >= greatest):
			temp = i;

	# Test
	test=pd.read_csv("test.csv")

	#test = test.drop(["date","winner"], axis=1,inplace=False)

	test.replace(encode, inplace=True)


	out = model[temp].predict(test)

	return out
