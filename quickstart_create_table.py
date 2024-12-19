# tag::wholeScript[]
from quickstart_connect import connect_to_database  # <1>
from astrapy.info import (
    CreateTableDefinition,
    ColumnType,
    VectorServiceOptions,
)

def main():
    database = connect_to_database()

    table_definition = (
        CreateTableDefinition.builder()
        # define all of the columns in the table
        .add_column("title", ColumnType.TEXT)
        .add_column("author", ColumnType.TEXT)
        .add_column("numberOfPages", ColumnType.INT)
        .add_column("rating", ColumnType.FLOAT)
        .add_column("publicationYear", ColumnType.INT)
        .add_column("summary", ColumnType.TEXT)
        .add_set_column(
            "genres",
            ColumnType.TEXT,
        )
        .add_map_column(
            "metadata",
            # key type
            ColumnType.TEXT,
            # value type
            ColumnType.TEXT,
        )
        .add_column("isCheckedOut", ColumnType.BOOLEAN)
        .add_column("borrower", ColumnType.TEXT)
        .add_column("dueDate", ColumnType.DATE)
        # also define a vector column. the dataset does not include vector data, but will autogenerate vector embeddings when we add rows to the table
        .add_vector_column(
            "summaryGenresVector",
            dimension=1024,
            service=VectorServiceOptions(
                provider="nvidia",
                # todo change model name if needed depending on the model deprecation timing
                model_name="NV-Embed-QA",
            )
        )
        # define the primary key. In this case, a composite primary key
        .add_partition_by(["title", "author"])
        # and finally build the table definition
        .build()
    )

    table = database.create_table(
        "quickstart_table",
        definition=table_definition,
    )

    print("Created table")

    table.create_index(
        "rating_index",
        column="rating",
    )

# todo need to tell people that need to wait to do finds until the index is created. is there a way to check? maybe list indexes? also should update the create index docs


if __name__ == "__main__":
    main()
# end::wholeScript[]