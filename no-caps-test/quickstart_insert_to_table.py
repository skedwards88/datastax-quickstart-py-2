from quickstart_connect import connect_to_database
from astrapy.data_types import (DataAPIDate, DataAPIMap, DataAPISet)
import json

def main():
    database = connect_to_database()

    table = database.get_table("quickstart_table_no_caps")

    data_file_path = "no-caps-test/data.json"

    with open(data_file_path, "r", encoding="utf8") as file:
        json_data = json.load(file)

    rows = [
        {
            **data,
            "genres": DataAPISet(data['genres']),
            "metadata": DataAPIMap(data['metadata']),
            "due_date": DataAPIDate.from_string(data['due_date']) if data.get('due_date') else None,
            "summary_genres_vector": (
                f"summary: {data['summary']} | "
                f"genres: {', '.join(data['genres'])}"
            ),
        }
        for data in json_data
    ]

    insert_result = table.insert_many(rows)

    print(f"Inserted ${len(insert_result.inserted_ids)} rows")


if __name__ == "__main__":
    main()
