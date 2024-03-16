# Online Health Enquiry Chatbot (STAT4011 Group Project)
<br>

if you want to reproduce the project, you can use git clone to get the source code.

# Code desription
- traditional.py is the code to implement the symptoms to disease prediction
- input_process.py is the intermediate program to decide the version of model (traditional/advanced)
- GUI.py is the PyQt5 class to generate GUI.
- disease-symptom-prediction-ml-99.ipynb is the visualization and model selection part in the chatbot development,
  it will produce the working/random_forest.joblib model which is called in traditional.py. You may generate your own model in the notebook.
  it would not be used in the chatbot
  (是从Kaggle上抄的。后面再改改)


# 1. Create a conda virtual environment
```bash
conda env create -f environment.yml
```
<br>

# 2. Run api_generate.py to generate the GLOVE model we used in the program. The model will be prepared under the directory ./working

<br>

# 3. Run the main.py to use the chatbot

