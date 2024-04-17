import re
import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import csv
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

training = pd.read_csv('data/training.csv')
training = training[training['prognosis'] != 'AIDS']
cols= training.columns
cols= cols[:-1]
x = training[cols]
y = training['prognosis']

reduced_data = training.groupby(training['prognosis']).max()

le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

clf1  = DecisionTreeClassifier()
clf = clf1.fit(x,y)

description_list = dict()
precautionDictionary=dict()

symptoms_dict = {}

for index, symptom in enumerate(cols):
       symptoms_dict[symptom] = index


def getDescription():
    global description_list
    with open('data/symptom_Description.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _description={row[0]:row[1]}
            description_list.update(_description)

def getprecautionDict():
    global precautionDictionary
    with open('data/symptom_precaution.csv', mode='r', encoding='utf-8') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec={row[0]:[row[1],row[2],row[3],row[4]]}
            precautionDictionary.update(_prec)

def check_pattern(dis_list,inp):
    pred_list=[]
    inp=inp.replace(' ','_')
    patt = f"{inp}"
    regexp = re.compile(patt)
    pred_list=[item for item in dis_list if regexp.search(item)]
    if(len(pred_list)>0):
        return 1,pred_list
    else:
        return 0,[]

def sec_predict(symptoms_exp):
    df = pd.read_csv('data/training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
      input_vector[[symptoms_dict[item]]] = 1

    return rf_clf.predict([input_vector])

def print_disease(node):
    node = node[0]
    val  = node.nonzero() 
    disease = le.inverse_transform(val[0])
    return list(map(lambda x:x.strip(),list(disease)))

tree_ = clf.tree_
feature_name = [
    cols[i] if i != _tree.TREE_UNDEFINED else "undefined!"
    for i in tree_.feature
]

chk_dis=",".join(cols).split(",")

def get_poss_symptom(symptom_input):
    conf, cnf_dis = check_pattern(chk_dis, symptom_input)
    output = "searches related to input: \n"
    for num, item in enumerate(cnf_dis):
        num += 1
        output += f"{num}) {item}\n"
    if len(cnf_dis) == 1:
        output += f"Is this the symptom you are experiencing? (type 1 to continue):  \n\n if none type 0 to search again."
    else:
        output += f"Select the one you meant (1 - {len(cnf_dis)}):  \n\n if none type 0 to search again."
    return output, conf

symptoms_present = []
def recurse(node, depth, symptom_input=None):
    if tree_.feature[node] != _tree.TREE_UNDEFINED:
        name = feature_name[node]
        threshold = tree_.threshold[node]

        if name == symptom_input:
            val = 1
        else:
            val = 0
        if  val <= threshold:
            return recurse(tree_.children_left[node], depth + 1)
        else:
            symptoms_present.append(name)
            return recurse(tree_.children_right[node], depth + 1)
    else:
        present_disease = print_disease(tree_.value[node])
        # print("predicted disease is ", present_disease)
        red_cols = reduced_data.columns
        symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
        # print("symptoms present in the patient are :" , symptoms_given)
        return list(symptoms_given), present_disease
    
def get_advise(user_report, present_disease):
    second_prediction = sec_predict(user_report)
    output = ""

    if present_disease[0] == second_prediction[0]:
        output += "You may have " + present_disease[0] + "\n"
        output += description_list[present_disease[0]] + "\n"
    else:
        output += "You may have " + present_disease[0] + " or " + second_prediction[0] + "\n"
        output += description_list[present_disease[0]] + "\n"
        output += description_list[second_prediction[0]] + "\n"

    precution_list = precautionDictionary[present_disease[0]]
    output += "\nTake following measures:\n\n"
    for i, j in enumerate(precution_list):
        if j != "":
            output += str(i+1) + ") " + j + "\n"
    output += "\nType anything to continue."
    return output

getDescription()
getprecautionDict()

if __name__ == "__main__":
    raise Exception("This file is not meant to run")