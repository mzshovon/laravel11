from Model.Contracts.ModelInterface import ModelInterface
from Model.Classes.GeminiModel import GeminiModel
from Model.Classes.LocalLLModel import LocalLLModel

class ModelFactory:
    @staticmethod
    def create_model(model: str, prompt: str) -> ModelInterface:
        if model == "gemini":
            return GeminiModel(model, prompt)
        elif model == "ollama":
            return LocalLLModel(model, prompt)
        else:
            raise ValueError("Unsupported model type")