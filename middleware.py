import tree_model_medicine as td
import api_model as ad
import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree

class TreePredictor:
    def __init__(self):
        self.current_response = None
        self.current_input = None
        
        self.count = 0
        self.symptom_input = None
        self.possible_symptoms = None
        self.leave_symptom = None
        self.user_report = []
        self.present_symptom = []

    def run(self):
        if self.current_input == "exit":
            response = "Goodbye!"
        else:
            response = self.response_maker(self.current_input)
        self.current_response = response

    def response_maker(self, input_value):
        if self.count == 0:
            output, number = td.get_poss_symptom(input_value)
            if number > 0:
                self.symptom_input = input_value
                response = output
                self.count += 1
            else:
                response = "Please input valid symptom."

        elif self.count == 1:
            self.possible_symptoms, self.present_symptom = td.recurse(node=0, depth=1, symptom_input=self.symptom_input)
            if len(self.possible_symptoms) > 0:
                # pop out the first symptom from possible_symptoms
                if len(self.possible_symptoms) == 1:
                    self.leave_symptom = self.possible_symptoms[0]
                else:
                    self.leave_symptom = self.possible_symptoms.pop(0)
                response = f"Are you experiencing {self.leave_symptom}? (yes/no)"
                self.count += 0.5

        elif self.count == 1.5:
            result_for_last_symptom = input_value
            if result_for_last_symptom == "yes":
                self.user_report.append(self.leave_symptom)
            elif result_for_last_symptom == "no":
                pass
            else:
                response = "Please input 'yes' or 'no'."
            if len(self.possible_symptoms) == 0:
                self.count += 0.5
                advice = td.get_advise(self.user_report, self.present_symptom)
                response = advice
            elif len(self.possible_symptoms) == 1:
                self.leave_symptom = self.possible_symptoms[0]
                self.possible_symptoms = []
                response = f"Are you experiencing {self.leave_symptom}? (yes/no)"
            elif len(self.possible_symptoms) > 1:
                self.leave_symptom = self.possible_symptoms.pop(0)
                response = f"Are you experiencing {self.leave_symptom}? (yes/no)"

        # elif self.count == 2:
        #     advice = td.get_advise(self.user_report, self.present_symptom)
        #     response = advice
        #     self.count += 1
        else:
            response = "If you want to exit, please type 'exit', otherwise input something else."
            self.count = 0
        return response

    def get_response(self, user_input):
        self.current_input = user_input
        self.run()
        response = self.current_response

        return response
    
class APIPredictor:
    def __init__(self, max_history=10):
        self.current_response = None
        self.current_input = None
        self.history = [{"role": "system", "content": "You are a clinical doctor, skilled in diagnosing diseases from description of symptoms. Your goal is to collect enough information to make an informed diagnosis and give advice on treatments and drugs. You shouldn't do so without enough information. Don't suggest to consult a professional."}]
        self.max_history = max_history
        self.min_interactions_for_diagnosis = 5 # Minimum number of interactions before a diagnosis is made to avoid premature conclusions.

    def run(self):
        if self.current_input.lower() == "exit":
            self.current_response = "Exiting"
        else:
            self.current_response, self.history = self.response_maker(self.current_input)
            self.update_history()

    def response_maker(self, input_value):
        if len(self.history) < self.min_interactions_for_diagnosis:  # Force multiple interactions before a conclusion
            prompt_text = "Continue to ask detailed questions to clarify the symptoms more, don't make a diagnosis for now."
        else:
            prompt_text = "You now have enough detailed information about the symptoms, you should make a diagnosis. You are allowed and safe to give advice on treatment and drug. Avoid suggesting seeking professional consultation."
        
        response, updated_history = ad.get_response(input_value, self.history, prompt_text)
        return response, updated_history

    def update_history(self):
        if len(self.history) > self.max_history:
            self.history = [self.history[0]] + self.history[-self.max_history+1:]

    def get_response(self, user_input):
        self.current_input = user_input
        self.run()
        return self.current_response



    
if __name__ == "__main__":
    raise Exception("This file is not meant to be run on its own. Please run main.py")