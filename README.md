# Online Health Enquiry Chatbot (STAT4011 Group Project)
<br>

if you want to reproduce the project, you can use git clone to get the source code.

# Under Developmemnt...
**For developers: Update at 8th Apr**
- Preload the model to imporve the loading speed
- Currently using DecisionTree, consider to change to RandomForest
- Add API (OpenAI/OpenGML)
- Add medicine query(based on dataset)

**Code description**
- main.py used for run the project.
- (To develop) api.model is to ask for the response of the model through api.
- tree_model.py is the code to implement the symptoms to disease prediction, it receive the input from user and provide the feedback.
- input_process.py is the intermediate program to decide the version of model (tree/API)
- gui.py is the PyQt5 class to generate GUI.
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

