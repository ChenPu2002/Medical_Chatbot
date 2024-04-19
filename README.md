# Online Health Enquiry Chatbot (STAT4011 Group Project)
<br>

if you want to reproduce the project, you can use git clone to get the source code and ADD OPENAI API KEY in .env
# To develop, PLEASE pull from main branch, here are codes for constructing a dev branch on your local repository

# Under Developmemnt...
**For developers: Update at 19th Apr**
- Preload the model to imporve the loading speed (cp) (Done)
- Rather than using one-word detect, we can still use a pre-trained word enbemdding model to accept a whole sentence as input. (alex)
- Currently using DecisionTree, consider to change to RandomForest (cp) (Done)
- Add API (OpenAI/OpenGML) (fys,tyy) (Done)
- Add medicine query (based on dataset) 
- Add visualization
- ~~consider to use pretrained similarity for diseases and sympotoms (Not to do)~~

**Simulate response**
- Tree model type 2 (medicine)
  
**Code description**
- main.py used for run the project.
- api.model is to ask for the response of the model through api.
- tree_model_medicine.py is the code to implement the symptoms to disease prediction, it receive the input from user and provide the feedback.
- input_process.py is the intermediate program to decide the version of model (tree/API)
- gui.py is the PyQt5 class to generate GUI.
- random_forest_generator.py is the file to generate the pretrained models.
- .env is used for store the API key (PLEASE add your own OPENAI API key in this file)
- inference_model_training.ipynb is model selection part in the chatbot development. (Not used) (More visualization should be done)
<br>

1. Create a conda virtual environment
```bash
conda env create -f environment.yml
```
Then activate the virtual environment
```bash
conda activate medical_chatbot
```
if you want to exit the virtual environment
```bash
conda deactivate
```
<br>

<!-- 2. Run api_generate.py to generate the GLOVE model we used in the program. The model will be prepared under the directory ./working -->

2. Run the main.py to use the chatbot

