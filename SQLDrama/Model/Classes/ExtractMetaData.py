import re

class ExtractMetaData:

    DATABASE_METADATA = {
        "users": {
            "columns": ["id", "name", "email", "contact", "email_verified_at", "created_at", "updated_at"],
            "primary_key": "id",
        },
        "payments": {
            "columns": ["id", "payment_channel", "trans_id", "amount", "status", "ip", "user_id", "created_at", "updated_at"],
            "foreign_keys": {"user_id": "users.id"},
        },
        "membership_details": {
            "columns": ["id", "first_name", "last_name", "nid", "membership_id", "dob", "address", "blood_group", "batch",
                        "employeer_name", "designation", "reference", "reference_number", "user_id", "payment",
                        "created_at", "updated_at"],
            "foreign_keys": {"user_id": "users.id"},
        }
    }

    def __init__(self, prompt:str):
        self.prompt = prompt


    def extract_metadata_from_prompt(self):
        prompt = self.prompt.lower()
        selected_tables = set()
        selected_columns = {}
        joins = []

        # Identify relevant tables based on keywords
        for table, meta in self.DATABASE_METADATA.items():
            for column in meta["columns"]:
                if column in prompt or table in prompt:
                    selected_tables.add(table)
                    if table not in selected_columns:
                        selected_columns[table] = []
                    selected_columns[table].append(column)

        # Identify relationships (joins)
        for table in selected_tables:
            if "foreign_keys" in self.DATABASE_METADATA[table]:
                for fk, ref_table in self.DATABASE_METADATA[table]["foreign_keys"].items():
                    parent_table = ref_table.split(".")[0]  # Extract parent table name
                    if parent_table in selected_tables:  # If related table is also in the prompt
                        joins.append(f"{table}.{fk} = {ref_table}")

        # Return structured metadata
        return {
            "tables": list(selected_tables),
            "columns": selected_columns,
            "joins": joins,
        }
