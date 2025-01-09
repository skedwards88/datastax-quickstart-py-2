# tag::wholeScript[]
from quickstart_connect import connect_to_database  # <1>
from astrapy.data_types import (DataAPIDate, DataAPIMap, DataAPISet)
import json

def main():
    database = connect_to_database()

    table = database.get_table("quickstart_table")

    data_file_path = "data.json" # todo use placeholder instead
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

    print(len(insert_result.inserted_ids))
    print(insert_result.inserted_ids)


if __name__ == "__main__":
    main()
# end::wholeScript[]
