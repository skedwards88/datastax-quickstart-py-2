from quickstart_connect import connect_to_database
from astrapy.info import (
    CreateTableDefinition,
    ColumnType,
    VectorServiceOptions,
)
from astrapy.info import TableVectorIndexOptions
from astrapy.constants import VectorMetric

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
        # todo could just specify cosine here to make it easier for people to modify, even though the default is cosine
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
        "quickstart_table_caps", # todo tell people that they can change this
        definition=table_definition,
    )

    print("Created table")

    # index the columns that you want to sort and filter on
    # todo it takes a while for the index to be created. need to tell people that need to wait to do finds until the index is created, otherwise error is thrown. todo may be better to just write a function that calls listIndex every 10 sec until returning?
    table.create_index(
        "rating_index",
        column="rating",
    )

    table.create_index(
        "numberOfPages_index",
        column="numberOfPages",
    )

    table.create_vector_index(
        "summaryGenresVector_index",
        column="summaryGenresVector",
        options=TableVectorIndexOptions(
            metric=VectorMetric.COSINE,
        ),
    )


if __name__ == "__main__":
    main()
