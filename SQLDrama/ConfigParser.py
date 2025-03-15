import yaml
import os

class ConfigParser:
    def __init__(self, config_file: str):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Build absolute path to config file
        config_path = os.path.join(script_dir, config_file)
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

    def get(self, key_path: str, **kwargs):
        keys = key_path.format(**kwargs).split(".")
        data = self.config
        for key in keys:
            if isinstance(data, list):
                data = {item: value for d in data for item, value in d.items()}  # Convert list to dict
            data = data.get(key, None)
            if data is None:
                return None
        return data
