# import psycopg2
from sqlalchemy import select, Column, Integer, String, Date, ForeignKey, Table, MetaData, create_engine, func, Date, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
import random
from datetime import date, datetime

engine = create_engine("postgresql://postgres:postgres@localhost/hr")
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

Base = declarative_base()

class Client(Base):
    """Модель для таблиці client."""
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(30), nullable=False)
    phone_number = Column(Integer, nullable=False)

    # Зв'язок із таблицею booking
    bookings = relationship("Booking", back_populates="client")

    def __repr__(self):
        return f"<Client(client_id={self.client_id}, name={self.name}, phone_number={self.phone_number})>"


class Room(Base):
    """Модель для таблиці room."""
    __tablename__ = 'room'

    room_id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String(30), nullable=False)
    room_status = Column(String(30))

    # Зв'язок із таблицею booking
    bookings = relationship("Booking", back_populates="room")

    def __repr__(self):
        return f"<Room(room_id={self.room_id}, type={self.type}, room_status={self.room_status})>"


class Booking(Base):
    """Модель для таблиці booking."""
    __tablename__ = 'booking'

    booking_id = Column(Integer, primary_key=True, nullable=False)
    booking_status = Column(String(20), nullable=False)
    date = Column(Date)
    client_id = Column(Integer, ForeignKey('client.client_id'), nullable=False)
    room_id = Column(Integer, ForeignKey('room.room_id'))

    # Відношення до таблиць client та room
    client = relationship("Client", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")

    def __repr__(self):
        return (f"<Booking(booking_id={self.booking_id}, booking_status={self.booking_status}, "
                f"date={self.date}, client_id={self.client_id}, room_id={self.room_id})>")

class Model:

    def get_all_tables(self):
        metadata.reflect(bind=engine)
        return list(metadata.tables.keys())

    def get_all_columns(self, table_name):
        table = Table(table_name, metadata, autoload_with=engine)
        return [column.name for column in table.columns]
    
    def search_with_group_order(self, table_name, field_name, field_value, group_by_field, order_by_field, limit=None, offset=0):
        try:
            model = globals()[table_name.title()]  # Наприклад, для "booking" знайдеться клас "Booking"
            query = session.query(model).filter(getattr(model, field_name) == field_value)
            query = query.group_by(getattr(model, group_by_field))
            query = query.order_by(getattr(model, order_by_field))
            if limit:
                query = query.limit(limit)
            query = query.offset(offset)
            results = query.all()
            
            return results

        except Exception as e:
            print(f"Error: {e}")
            return []

    def fetch_table_data(self, table_name, offset=0, limit=10):
        """Отримання даних з таблиці з використанням OFFSET та LIMIT."""
        try:
            table = Table(table_name, metadata, autoload_with=engine)
            query = table.select().offset(offset).limit(limit)
            result = session.execute(query).fetchall()
            return result
        except Exception as e:
            print(f"Error fetching data from {table_name}: {e}")
        return []

    def add_data(self, table, columns, val):
        if table == 'client':
            self.add_client(columns, val)
        elif table == 'room':
            self.add_room(columns, val)
        elif table == 'booking':
            self.add_booking(columns, val)
        else:
            return "Таблиця не знайдена"
        return 1

    def add_client(self, columns, values):
        """Додавання запису в таблицю Client."""
        try:
            # Створюємо таблицю
            table = Table('client', Base.metadata, autoload_with=engine)
            
            # Створюємо запит для вставки даних
            insert_statement = table.insert().values(dict(zip(columns, values)))
            
            # Виконуємо запит
            session.execute(insert_statement)
            session.commit()
            print("Client added successfully.")
        except Exception as e:
            print(f"Error adding client: {e}")
            session.rollback()


    def add_room(self, columns, values):
        """Додавання запису в таблицю Room."""
        try:
            # Створюємо таблицю
            table = Table('room', Base.metadata, autoload_with=engine)
            
            # Створюємо запит для вставки даних
            insert_statement = table.insert().values(dict(zip(columns, values)))
            
            # Виконуємо запит
            session.execute(insert_statement)
            session.commit()
            print("Room added successfully.")
        except Exception as e:
            print(f"Error adding room: {e}")
            session.rollback()


    def add_booking(self, columns, values):
        """Додавання запису в таблицю Booking."""
        try:
            # Створюємо таблицю
            table = Table('booking', Base.metadata, autoload_with=engine)
            
            # Створюємо запит для вставки даних
            insert_statement = table.insert().values(dict(zip(columns, values)))
            
            # Виконуємо запит
            session.execute(insert_statement)
            session.commit()
            print("Booking added successfully.")
        except Exception as e:
            print(f"Error adding booking: {e}")
            session.rollback()


    def update_data(self, table_name, column, id, new_value):
        try:
            table = Table(table_name, metadata, autoload_with=engine)
            if column == f'{table_name.lower()}_id':
                existing_identifiers = [item[0] for item in session.query(table.c[column]).all()]
                if int(new_value) in existing_identifiers:
                    return 2
            elif column.endswith('_id'):
                referenced_table = column[:-3].capitalize()
                referenced_table = Table(referenced_table, metadata, autoload_with=engine)
                referenced_values = [item[0] for item in session.query(referenced_table.c[column]).all()]
                if int(new_value) not in referenced_values:
                    return 3
            identifier_column = f'{table_name.lower()}_id'
            session.query(table).filter(table.c[identifier_column] == id).update({column: new_value})
            session.commit()
            return 1
        except Exception as e:
            print(f"Error updating data: {e}")
            session.rollback()
        return 0

    def delete_data(self, table_name, id):
        try:
            table = Table(table_name, metadata, autoload_with=engine)
            for current_table in metadata.tables.values():
                if current_table.name == table_name:
                    continue
                for column in current_table.columns:
                    if column.name == f'{table_name.lower()}_id':
                        referenced_values = session.query(current_table.c[column.name]).filter(current_table.c[column.name] == id).all()
                        if referenced_values:
                            print(f"Row with ID: {id} used in another table.")
                            return 0
            session.query(table).filter(table.c[f'{table_name.lower()}_id'] == id).delete()
            session.commit()
            print(f"Row with ID: {id} successfully added to table: {table_name}.")
            return 1

        except Exception as e:
            print(f"Error deleting data: {e}")
            session.rollback()
        return 0

    def generate_data(self, table_name, count):
        try:
            table = Table(table_name, metadata, autoload_with=engine)
            id_column = f'{table_name.lower()}_id'
            for i in range(count):
                insert_values = {}
                for column in table.columns:
                    column_name = column.name
                    column_type = column.type
                    if column_name == id_column:
                        max_id = session.query(func.max(table.c[column_name])).scalar() or 0
                        insert_values[column_name] = max_id + 1
                    elif column_name == 'id_tab':
                        while True:
                            new_id_tab = random.randint(1, 1000) 
                            existing_id = session.query(table.c.id_tab).filter_by(id_tab=new_id_tab).first()
                            if not existing_id:
                                insert_values[column_name] = new_id_tab
                                break
                    elif column_name.endswith('_id'):
                        related_table_name = column_name[:-3]
                        related_table = Table(related_table_name, metadata, autoload_with=engine)
                        related_id = session.query(related_table.c[f'{related_table_name.lower()}_id']).order_by(func.random()).first()
                        insert_values[column_name] = related_id[0] if related_id else None
                    elif isinstance(column_type, Integer):
                        insert_values[column_name] = random.randint(1, 100)
                    elif isinstance(column_type, String):
                        insert_values[column_name] = f"Text {column_name}"
                    elif isinstance(column_type, Date):
                        insert_values[column_name] = date(2024, 1, 1)
                    elif isinstance(column_type, DateTime):
                        insert_values[column_name] = datetime(2024, 1, 1, 8, 30)
                session.execute(table.insert().values(insert_values))
            session.commit()
            print(f"{count} rows added to table: {table_name}.")
        except Exception as e:
            session.rollback() 
            print(f"Error during generating: {e}")