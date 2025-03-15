import sys
import destruct_response
import export
import uuid
import json
from Database import Database
from Model.Classes.ExtractMetaData import ExtractMetaData
from Model.Factories.ModelFactory import ModelFactory
from ConfigParser import ConfigParser

if len(sys.argv) < 4:
    print("Please provide valid parameters.")
    sys.exit(1)

prompt = sys.argv[1]
model = sys.argv[2]
export_type = sys.argv[3]
export_path = sys.argv[4]

prefix = "Give me MYSQL query for mariaDB supported on prompt: "


suffix = ExtractMetaData(prompt=prompt).extract_metadata_from_prompt()
final_prompt = f"{prefix}{prompt}. Below are the tables and relationships if needed: {suffix}"

model_instance = ModelFactory.create_model(model=model, prompt=final_prompt)
response = model_instance.generate()

db = Database(host="localhost", user="root", password="", database="alumni")

storytelling_text, sql_query = destruct_response.parse_response(response)

prompt_response = {
    "sql": sql_query,
    "story": storytelling_text
}

result = db.execute_query(sql_query)

if result is not None:
    extension = ConfigParser("config.yml").get(f"export_extension.{export_type}")
    key_point = uuid.uuid4()
    file_name = f"{export_path}\{key_point}-file.{extension}"
    # print(f"Generating {file_type} file.....")
    export.export_to_file(export_type, result, file_name)
    prompt_response['download'] = file_name

print(json.dumps(prompt_response))

