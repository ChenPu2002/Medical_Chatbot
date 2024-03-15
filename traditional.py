import joblib
import pandas as pd
import numpy as np

class TraditionalModel():
    def __init__(self, input_text):
        self.input_text = input_text
        self.output_text = self.process()
    
    def process(self):
        input_text = self.input_text
        output_text = self.predict(input_text)
        return output_text
    
    def predict(self, input_text):
        # load, no need to initialize the loaded_rf
        loaded_rf = joblib.load("working/random_forest.joblib")
        input_text = "itching"
        output = self.predd(loaded_rf, input_text)
        return output

    def predd(x,*args):
        # args = [symptom1, symptom2, symptom3, ...]
        psymptoms = [x for x in args]
        # append zero until 17 symptoms
        while len(psymptoms) < 17:
            psymptoms.append(0)

        discrp = pd.read_csv("archive/symptom_Description.csv")
        ektra7at = pd.read_csv("archive/symptom_precaution.csv")
        #print(psymptoms)
        df1 = pd.read_csv("symptom_severity.csv")
        a = np.array(df1["Symptom"])
        b = np.array(df1["weight"])
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
        for i in range(1,len(ektra7at.iloc[c])):
            precuation_list.append(ektra7at.iloc[c,i])
        print("The Disease Name: ",pred2[0])
        print("The Disease Discription: ",disp)
        print("Recommended Things to do at home: ")
        for i in precuation_list:
            print(i)

if __name__ == "__main__":
    input_text = "itching"
    print(TraditionalModel(input_text).precess())
    #raise ValueError("This file is not meant to be run directly. Run main.py instead.")