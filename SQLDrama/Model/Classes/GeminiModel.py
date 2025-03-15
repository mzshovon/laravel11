from Model.Contracts.ModelInterface import ModelInterface
from ConfigParser import ConfigParser
from google import genai

class GeminiModel(ModelInterface):


    def generate(self):
        [model_name, api_key] = self._get_config(self.model)
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=self.prompt,
        )
        return response.text

    def _get_config(self, model:str) -> dict:
        config = ConfigParser("config.yml")
        agent = config.get(f"agent.{model}")
        model_name = agent[0]['model']
        api_keys = agent[1]['api_key']
        return [model_name, api_keys]

