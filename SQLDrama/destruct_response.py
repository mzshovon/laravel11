import re

def parse_response(response):
    sql_pattern = r"```sql\n(.*?)\n```"
    sql_match = re.search(sql_pattern, response, re.DOTALL)

    sql_query = sql_match.group(1) if sql_match else ""

    # print(f"SQL ready for query: {sql_query}")

    # Remove the SQL block to get storytelling text
    text = re.sub(sql_pattern, "", response, flags=re.DOTALL).strip()
    storytelling_text = re.sub(r'\n+', '\n', text)


    # print(f"Text ready for story telling: {storytelling_text}")

    return storytelling_text, sql_query
