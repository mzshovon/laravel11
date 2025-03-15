import ollama
from Model.Contracts.ModelInterface import ModelInterface
from ConfigParser import ConfigParser

class LocalLLModel(ModelInterface):

    def generate(self)->str:
        model_name = self._get_config(self.model)
        response = ollama.generate(
            model=model_name,
            prompt=f"Convert the following prompt into MYSQL query: {self.prompt}"
        )
        return response['response']

    def _get_config(self, model:str) -> str:
        config = ConfigParser("config.yml")
        agent = config.get(f"agent.{model}")
        model_name = agent[0]['model']
        return model_name
