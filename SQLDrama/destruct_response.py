import re

def parse_response(response):
    sql_pattern = r"```sql\n(.*?)\n```"
    sql_match = re.search(sql_pattern, response, re.DOTALL)
    sql_query = sql_match.group(1) if sql_match else ""
    # Remove the SQL block to get storytelling text
    storytelling_text = re.sub(sql_pattern, "", response, flags=re.DOTALL).strip()
    return storytelling_text, sql_query
