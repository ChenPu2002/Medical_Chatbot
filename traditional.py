import joblib
import pandas as pd
import numpy as np
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TraditionalModel():
    def __init__(self, input_text):
        self.input_text = input_text
        self.df1 = pd.read_csv("symptom_severity.csv")
        self.preporcess()
        self.symptom_matching()
        self.output_text = self.predict()

    def preporcess(self):
        # 预处理步骤
        input_text = self.input_text.lower()  # 转换为小写
        input_text = re.sub(r'[^a-zA-Z0-9]', ' ', input_text)  # 去除标点符号
        tokens = self.input_text.split()  # 分词
        stop_words = set(stopwords.words('english'))  # 停用词列表
        # tokens = [word for word in tokens if word not in stop_words]  # 去除停用词

        lemmatizer = WordNetLemmatizer()
        self.input_text = [lemmatizer.lemmatize(word) for word in tokens]  # 词形还原

    # def process(self):
    #     input_text = self.input_text
    #     output_text = self.predict(input_text)
    #     return output_text
    def symptom_matching(self):
        a = np.array(self.df1["Symptom"])
        glove_model = KeyedVectors.load('working/glove-wiki-gigaword-100.model')
        symptom_vectors = np.array([glove_model[symptom] for symptom in a if symptom in glove_model])
        input_vector = np.mean([glove_model[word] for word in self.input_text if word in glove_model], axis=0)
        similarity_scores = cosine_similarity([input_vector], symptom_vectors)
        top_indices = similarity_scores.argsort()[0][-3:][::-1]
        self.input_text = [a[index] for index in top_indices]
    # def symptom_matching(self):
    #     a = np.array(self.df1["Symptom"])
    #     tfidf_vectorizer = TfidfVectorizer()
    #     symptom_texts = self.df1["Symptom"]
    #     symptom_texts = [' '.join(text) for text in symptom_texts] 
    #     symptom_tfidf = tfidf_vectorizer.fit_transform(symptom_texts)
    #     input_tfidf = tfidf_vectorizer.transform([self.input_text])
    #     similarity_scores = cosine_similarity(input_tfidf, symptom_tfidf)
    #     k = 3  # 要获取的最相似症状数量
    #     top_indices = similarity_scores.argsort()[0][-k:][::-1]
    #     top_symptoms = [symptom_texts[index] for index in top_indices]
    #     self.input_text = top_symptoms




    
    def predict(self):
        # load, no need to initialize the loaded_rf
        loaded_rf = joblib.load("working/random_forest.joblib")
        # input_text = "itching"
        output = self.predd(loaded_rf, self.input_text)
        return output

    def predd(self,x, psymptoms):
        # args = [symptom1, symptom2, symptom3, ...]
        #psymptoms = [x for x in args]
        # append zero until 17 symptoms
        while len(psymptoms) < 17:
            psymptoms.append(0)
        # psy = [3,5,3,5,4,4,3,2,3,0,0,0,0,0,0,0,0]
        #psy = np.array([psymptoms])

        discrp = pd.read_csv("archive/symptom_Description.csv")
        ektra7at = pd.read_csv("archive/symptom_precaution.csv")
        #print(psymptoms)

        a = np.array(self.df1["Symptom"])
        b = np.array(self.df1["weight"])
        for j in range(len(psymptoms)):
            for k in range(len(a)):
                if psymptoms[j]==a[k]:
                    psymptoms[j]=b[k]
        psy = [psymptoms]
        pred2 = x.predict(psy)
        disp= discrp[discrp['Disease']==pred2[0]]
        disp = disp.values[0][1]
        recomnd = ektra7at[ektra7at['Disease']==pred2[0]]
        c=np.where(ektra7at['Disease']==pred2[0])[0][0]
        precuation_list=[]
        import math
        for i in range(1,len(ektra7at.iloc[c])):
            if type(ektra7at.iloc[c,i])==str:
                precuation_list.append(ektra7at.iloc[c,i])
        # print(precuation_list)
        # print("The Disease Name: ",pred2[0])
        # print("The Disease Discription: ",disp)
        # print("Recommended Things to do at home: ")
        # for i in precuation_list:
        #     print(i)
        disease_name = "The Disease Name: " + pred2[0]
        disease_description = "The Disease Description: " + disp
        recommended_things = "I recommend you to do:\n" + "\n".join(precuation_list)

        output_string = disease_name + "\n" + disease_description + "\n" + recommended_things
        return output_string

if __name__ == "__main__":
    input_text = "I have itching and stomach pain"
    # print(TraditionalModel(input_text).output_text)
    raise ValueError("This file is not meant to be run directly. Run main.py instead.")