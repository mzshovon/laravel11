import pymysql

class Database:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        self.connect()

    def connect(self):
        """Establishes a connection to the database."""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.MySQLError as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

    def ensure_connection(self):
        """Reconnects if the connection is lost."""
        if self.connection is None or not self.connection.open:
            self.connect()

    def table_exists(self, table_name):
        """Checks if a table exists in the database."""
        self.ensure_connection()
        query = "SHOW TABLES LIKE %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (table_name,))
            return cursor.fetchone() is not None

    def execute_query(self, query, params=None, table_name=None):
        """
        Executes a SQL query. Ensures the connection and checks for the table if specified.

        :param query: The SQL query to execute.
        :param params: Parameters for the SQL query.
        :param table_name: (Optional) Table name to check before execution.
        :return: Query result for SELECT queries, or affected rows for others.
        """
        self.ensure_connection()

        if table_name and not self.table_exists(table_name):
            print(f"Table '{table_name}' does not exist.")
            return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params if params else None)
                if query.strip().lower().startswith("select"):
                    return cursor.fetchall()
                self.connection.commit()
                return cursor.rowcount
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
            return None

    def close(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
