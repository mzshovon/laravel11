import sys
import json
import generate
import destruct_response
import export
from Database import Database
import uuid

if len(sys.argv) < 2:
    print("Please provide a prompt.")
    sys.exit(1)

prompt = sys.argv[1]

# print(f"Received prompt: {prompt}")



file_type = "csv"
prefix = uuid.uuid4()
file_name = f"{prefix}-file.csv"
path = "E:/TukTechs/PROJECTS/htdocs/laravel11/storage/temp/"
file_path= f"{path}{file_name}"

db = Database(host="localhost", user="root", password="", database="alumni")

response = generate.generate(prompt)

storytelling_text, sql_query = destruct_response.parse_response(response)

prompt_response = {
    "sql": sql_query,
    "story": storytelling_text
}

result = db.execute_query(sql_query)

if result is not None:
    # print(f"Generating {file_type} file.....")
    export.export_to_csv(result, file_path)
    prompt_response['download'] = file_name

print(json.dumps(prompt_response))

