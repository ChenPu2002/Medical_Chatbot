import tree_model_medicine as td
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
        self.poss_list = None

    def run(self):
        if self.current_input == "exit":
            response = "Goodbye!"
        else:
            response = self.response_maker(self.current_input)
        self.current_response = response

    def response_maker(self, input_value):
        if self.count == 0:
            output, number, self.poss_list = td.get_poss_symptom(input_value)
            if number > 0:
                # self.symptom_input = input_value
                response = output
                self.count += 1
            else:
                response = "Please input valid symptom."

        elif self.count == 1:
            # change input_value to number
            input_value = input_value.strip()
            # check if input_value is number
            if input_value.isdigit() and int(input_value) >= 0:
                self.symptom_input = self.poss_list[int(input_value) - 1]
                self.possible_symptoms, self.present_symptom = td.recurse(node=0, depth=1, symptom_input=self.symptom_input)
                if len(self.possible_symptoms) > 0:
                    # pop out the first symptom from possible_symptoms
                    if len(self.possible_symptoms) == 1:
                        self.leave_symptom = self.possible_symptoms[0]
                    else:
                        self.leave_symptom = self.possible_symptoms.pop(0)
                    response = f"Are you experiencing {self.leave_symptom}? (yes/no)"
                    self.count += 0.5
            else:
                response = "Please choose a symptom by number."

        elif self.count == 1.5:
            result_for_last_symptom = input_value
            if result_for_last_symptom == "yes" or result_for_last_symptom == "no":
                if result_for_last_symptom == "yes":
                    self.user_report.append(self.leave_symptom)
                elif result_for_last_symptom == "no":
                    pass

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
            else:
                # recover the symptom to the possible_symptoms
                if self.leave_symptom not in self.possible_symptoms:
                    self.possible_symptoms.insert(0, self.leave_symptom)
                response = "Please input 'yes' or 'no'. (Type yes to continue)"
        else:
            response = "If you want to exit, please type 'exit', otherwise type another symptom."
            self.count = 0
        return response

    def get_response(self, user_input):
        self.current_input = user_input
        self.run()
        response = self.current_response

        return response
    
class APIPredictor:
    def __init__(self):
        self.current_response = None
        self.current_input = None

    def run(self):
        if self.current_input == "exit":
            response = "Goodbye!"
        else:
            response = self.response_maker(self.current_input)
        self.current_response = response

    def response_maker(self, input_value):
        response = "This is the response from the API to the input: " + input_value
        return response

    def get_response(self, user_input):
        self.current_input = user_input
        self.run()
        response = self.current_response

        return response
    
if __name__ == "__main__":
    raise Exception("This file is not meant to be run on its own. Please run main.py")