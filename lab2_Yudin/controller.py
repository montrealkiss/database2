import sys

from model import Model
from view import View


class Controller:
    def __init__(self):
        self.view = View()
        try:
            self.model = Model()
            self.view.show_message("Connecting to DB...")
        except Exception as e:
            self.view.show_message(f"Error druing initializtion {e}")
            sys.exit(1)

    def run(self):
        while True:
            choice = self.view.show_menu()
            if choice == '1':
                self.view_tables()
            elif choice == '2':
                self.view_columns()
            elif choice == '3':
                self.view_table_data()
            elif choice == '4':
                self.add_data()
            elif choice == '5':
                self.update_data()
            elif choice == '6':
                self.delete_data()
            elif choice == '7':
                self.generate_data()
            elif choice == '8':
                self.get_search_group_by_input()
            elif choice == '9':
                break

    def view_tables(self):
        tables = self.model.get_all_tables()
        self.view.show_tables(tables)

    def view_columns(self):
        table_name = self.view.ask_table()
        columns = self.model.get_all_columns(table_name)
        self.view.show_columns(columns)

    def view_table_data(self):
        table_name = self.view.ask_table()
        offset = int(self.view.inp("Enter starting row (offset): "))
        limit = int(self.view.inp("Enter number of rows to fetch (limit): "))
        data = self.model.fetch_table_data(table_name, offset, limit)
        self.view.show_table_data(data)

    def get_search_group_by_input(self):
        try:
            table_name = self.view.inp("Enter table name: ")
            field_name = self.view.inp("Enter column name to search in: ")
            field_value = self.view.inp("Enter value to search: ")
            group_by_field = self.view.inp("Enter field to group by: ")
            order_by_field = self.view.inp("Enter field to order by: ")
            limit = input("Enter limit of search result (or leave blank for no limit): ").strip()
            limit = int(limit) if limit not in ['', ' '] else None
            results = self.model.search_with_group_order(table_name, field_name, field_value, group_by_field, order_by_field, limit)

            if results:
                self.view.show_message("Results:")
                if table_name == 'client':
                    self.view.show_client(results)
                elif table_name == 'room':
                    self.view.show_room(results)
                elif table_name == 'booking':
                    self.view.show_booking(results)  
            else:
                self.view.show_message("Not found")

        except Exception as e:
            self.view.show_message(f"Error: {e}")
        

    def add_data(self):
        while True:
            table, columns, val = self.view.insert()
            error = self.model.add_data(table, columns, val)
            if int(error) == 1:
                self.view.show_message("Data successfully added!")
                agree = self.view.ask_continue()
                if agree == 'n':
                    break
            elif int(error) == 2:
                self.view.show_message("ID already existing")
                agree = self.view.ask_continue()
                if agree == 'n':
                    break
            else:
                self.view.show_message("Wrong FK key")
                agree = self.view.ask_continue()
                if agree == 'n':
                    break

    def update_data(self):
        while True:
            table, column, id, new_value = self.view.update()
            error = self.model.update_data(table, column, id, new_value)
            if int(error) == 1:
                self.view.show_message("Data successfully added!")
                agree = self.view.ask_continue()
                if agree == 'n':
                    break
            elif int(error) == 2:
                self.view.show_message(f"ID {new_value} already existing")
                agree = self.view.ask_continue()
                if agree == 'n':
                    break
            else:
                self.view.show_message(f"Wrong FK key: {new_value} in column: {column}")
                agree = self.view.ask_continue()
                if agree == 'n':
                    break

    def delete_data(self):
        while True:
            table, id = self.view.delete()
            error = self.model.delete_data(table, id)
            if int(error) == 1:
                self.view.show_message("Row deleted")
                agree = self.view.ask_continue()
                if agree == 'n':
                    break
            else:
                self.view.show_message("Impossible to delete row while some other reffering to it")
                agree = self.view.ask_continue()
                if agree == 'n':
                    break

    def generate_data(self):
        table_name, num_rows = self.view.generate_data_input()
        self.model.generate_data(table_name, num_rows)
        self.view.show_message(f"Data for table: {table_name} was generated sucessfully!")
