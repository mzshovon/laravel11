from abc import ABC, abstractmethod

class ModelInterface:
    def __init__(self, model:str, prompt:str):
        self.model = model
        self.prompt = prompt
        
    @abstractmethod
    
    def generate()->str:
        pass