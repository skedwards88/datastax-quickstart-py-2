# tag::wholeScript[]
from quickstart_connect import connect_to_database  # <1>
from astrapy.info import (
    CreateTableDefinition,
    ColumnType,
    VectorServiceOptions,
)
from astrapy.info import TableIndexOptions, TableVectorIndexOptions
from astrapy.constants import VectorMetric

def main():
    database = connect_to_database()

    table_definition = (
        CreateTableDefinition.builder()
        # define all of the columns in the table
        .add_column("title", ColumnType.TEXT)
        .add_column("author", ColumnType.TEXT)
        .add_column("number_of_pages", ColumnType.INT)
        .add_column("rating", ColumnType.FLOAT)
        .add_column("publication_year", ColumnType.INT)
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
        .add_column("is_checked_out", ColumnType.BOOLEAN)
        .add_column("borrower", ColumnType.TEXT)
        .add_column("due_date", ColumnType.DATE)
        # also define a vector column. the dataset does not include vector data, but will autogenerate vector embeddings when we add rows to the table
        # todo could just specifiy cosine here to make it easier for people to modify, even though the default is cosine
        .add_vector_column(
            "summary_genres_vector",
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
        "quickstart_table_snake",
        definition=table_definition,
    )

    print("Created table")

# index the columns that you want to sort and filter on
# todo it takes a while for the index to be created. need to tell people that need to wait to do finds until the index is created, otherwise error is thrown. is there a way to check? maybe list indexes? also should update the create index docs
    table.create_index(
        "rating_snake_index",
        column="rating",
    )

    table.create_index(
        "number_of_pages_snake_index",
        column="number_of_pages",
    )

    table.create_vector_index(
        "summary_genres_vector_snake_index",
        column="summary_genres_vector",
        options=TableVectorIndexOptions(
            metric=VectorMetric.COSINE,
        ),
    )

if __name__ == "__main__":
    main()
# end::wholeScript[]
