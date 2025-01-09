from quickstart_connect import connect_to_database
from astrapy.data_types import (DataAPIDate, DataAPIMap, DataAPISet)
import json

def main():
    database = connect_to_database()

    table = database.get_table("quickstart_table_caps")

    data_file_path = "caps-test/data.json"

    with open(data_file_path, "r", encoding="utf8") as file:
        json_data = json.load(file)

    rows = [
        {
            **data,
            "genres": DataAPISet(data['genres']),
            "metadata": DataAPIMap(data['metadata']),
            "dueDate": DataAPIDate.from_string(data['dueDate']) if data.get('dueDate') else None,
            "summaryGenresVector": (
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
