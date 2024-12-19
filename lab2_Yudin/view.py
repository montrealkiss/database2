import time


class View:
    def show_menu(self):
        while True:
            print("Menu:")
            print("1. Get table names")
            print("2. Get table column names ")
            print("3. Get table data")
            print("4. Add data to table")
            print("5. Update data in table")
            print("6. Remove data from table")
            print("7. Generate data")
            print("8. Search data")
            print("9. Quit")

            choice = input("Option: ")

            if choice in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                return choice
            else:
                print("Please enter correct choice in range (from 1 to 8)")
                time.sleep(2)

    def show_message(self, message):
        print(message)
        time.sleep(2)

    def ask_continue(self):
        agree = input("Continue making changes? (y/n) ")
        return agree

    def show_tables(self, tables):
        print("Table names:")
        for table in tables:
            print(table)
        time.sleep(2)

    def ask_table(self):
        table_name = input("Enter table name: ")
        return table_name

    def inp(self, message):
        inp = input(message)
        return inp

    def show_table_data(self, data):
        if not data:
            print("No data found or an error occurred.")
        else:
            for row in data:
                print(row)

    def show_columns(self, columns):
        print("Column names:")
        for column in columns:
            print(column)
        time.sleep(2)

    def show_booking(self, data):
        """Форматований вивід для таблиці booking."""
        for row in data:
            print(f"Booking ID: {row.booking_id}")
            print(f"Status: {row.booking_status}")
            print(f"Date: {row.date}")
            print(f"Client ID: {row.client_id}")
            print(f"Room ID: {row.room_id}\n")
    
    def show_client(self, data):
        """Форматований вивід для таблиці client."""
        for row in data:
            print(f"Client ID: {row.client_id}")
            print(f"Name: {row.name}")
            print(f"Phone Number: {row.phone_number}\n")

    def show_room(self, data):
        """Форматований вивід для таблиці room."""
        for row in data:
            print(f"Room ID: {row.room_id}")
            print(f"Type: {row.type}")
            print(f"Status: {row.room_status}\n")

    def insert(self):
        while True:
            try:
                table = input("Enter table name: ")
                columns = input("Enter column names (with space between): ").split()
                val = input("Enter values according to columns order (with space between): ").split()

                if len(columns) != len(val):
                    raise ValueError("Columns and values aren't matching")

                return table, columns, val
            except ValueError as e:
                print(f"Error: {e}")

    def update(self):
        while True:
            try:
                table = input("Enter table name: ")
                column = input("Enter column name: ")
                id = int(input("Enter row ID to change: "))
                new_value = input("Enter new value: ")
                return table, column, id, new_value
            except ValueError as e:
                print(f"Error: {e}")

    def delete(self):
        while True:
            try:
                table = input("Enter table name: ")
                id = int(input("Enter row ID to delete: "))
                return table, id
            except ValueError as e:
                print(f"Error: {e}")

    def generate_data_input(self):
        while True:
            try:
                table_name = input("Enter table name: ")
                num_rows = int(input("Enter row quantity to generate: "))
                return table_name, num_rows
            except ValueError as e:
                print(f"Error: {e}")
