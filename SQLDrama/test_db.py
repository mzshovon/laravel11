from Database import Database

db = Database(host="localhost", user="root", password="", database="alumni")

# Check if a table exists
print(db.table_exists("users"))

# Execute a SELECT query
result = db.execute_query("SELECT * FROM users", table_name="users")
print(result)

# Execute an INSERT query
# rows_affected = db.execute_query("INSERT INTO users (name, email) VALUES (%s, %s)", ("John Doe", "john@example.com"), table_name="users")
# print(f"Rows affected: {rows_affected}")

db.close()