from quickstart_connect import connect_to_database

def main():
    database = connect_to_database()

    names = database.list_table_names()

    for name in names:
      print(name)
      database.drop_table(name)

if __name__ == "__main__":
    main()
