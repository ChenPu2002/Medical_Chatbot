from traditional import TraditionalModel
class InputProcess():
    def __init__(self, input_text, model):
        self.input_text = input_text
        self.model = model
        # self.output_text = self.processInput()
    
    def process(self):
        input_text = self.input_text
        if self.model == 'Traditional Model': 
            output_text = TraditionalModel(input_text).process()
        elif self.model == 'Advanced Model':
            output_text = 'Still in development...'
        else:
            raise ValueError('Model not found')
        return output_text

if __name__ == "__main__":
    raise ValueError("This file is not meant to be run directly. Run main.py instead.")
    