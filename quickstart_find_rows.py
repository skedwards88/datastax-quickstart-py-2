from quickstart_connect import connect_to_database
from astrapy.info import TableIndexOptions, TableVectorIndexOptions
from astrapy.constants import VectorMetric

def main():
    database = connect_to_database()

    table = database.get_table("quickstart_table2") # todo revert 2

    # table.create_index(
    #     "winner_index",
    #     column="winner",
    #     options=TableIndexOptions(
    #         ascii=False,
    #         normalize=True,
    #         case_sensitive=False,
    #     ),
    # )

    # table.create_vector_index(
    #     "m_vector_index",
    #     column="m_vector",
    #     options=TableVectorIndexOptions(
    #         metric=VectorMetric.DOT_PRODUCT,
    #     ),
    # )

    # Find documents that match a filter
    print("\nFinding books with rating greater than 4.7...")

    rating_cursor = table.find({"rating": {"$gt": 4.7}}) # todo change duration_cursor var name in current quickstart

    for row in rating_cursor:
        print(f"{row['title']} is rated {row['rating']}")

    # Perform a vector search to find the closest match to a search string
    print("\nUsing vector search to find a single scary novel...")

    single_vector_match = table.find_one(
        {}, sort={"$vectorize": "A scary novel"}
    )

    print(f"{single_vector_match['title']} is a scary novel")

    # # Combine a filter, vector search, and projection to find the 3 books with
    # # more than 400 pages that are the closest matches to a search string,
    # # and just return the title and author
    # print("\nUsing filters and vector search to find 3 books with more than 400 pages that are set in the arctic, returning just the title and author...")

    # vector_cursor = collection.find(
    #     {"numberOfPages": {"$gt": 400}},
    #     sort={"$vectorize": "A book set in the arctic"},
    #     limit=3,
    #     projection={"title": True, "author": True}
    # )

    # for row in vector_cursor:
    #     print(row)


if __name__ == "__main__":
    main()
