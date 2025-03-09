# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
# from sqlalchemy.orm import declarative_base, relationship, Session
# from dotenv import load_dotenv
# import os

# # Загружаем переменные из .env файла
# load_dotenv()

# # Получаем параметры подключения из переменных окружения
# db_name = os.getenv('DB_NAME')
# db_user = os.getenv('DB_USER')
# db_password = os.getenv('DB_PASSWORD')
# db_host = os.getenv('DB_HOST')
# db_port = os.getenv('DB_PORT')

# # Формируем строку подключения
# connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
# engine = create_engine(connection_string, echo=True)

# # Создаем базовый класс для моделей
# Base = declarative_base()

# # Определяем модели
# class Publisher(Base):
#     __tablename__ = 'publisher'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     books = relationship("Book", back_populates="publisher")

# class Book(Base):
#     __tablename__ = 'book'
#     id = Column(Integer, primary_key=True)
#     title = Column(String, nullable=False)
#     id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)
#     publisher = relationship("Publisher", back_populates="books")
#     stocks = relationship("Stock", back_populates="book")

# class Shop(Base):
#     __tablename__ = 'shop'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     stocks = relationship("Stock", back_populates="shop")

# class Stock(Base):
#     __tablename__ = 'stock'
#     id = Column(Integer, primary_key=True)
#     id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
#     id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
#     count = Column(Integer, nullable=False)
#     book = relationship("Book", back_populates="stocks")
#     shop = relationship("Shop", back_populates="stocks")
#     sales = relationship("Sale", back_populates="stock")

# class Sale(Base):
#     __tablename__ = 'sale'
#     id = Column(Integer, primary_key=True)
#     price = Column(Integer, nullable=False)
#     date_sale = Column(Date, nullable=False)
#     id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
#     count = Column(Integer, nullable=False)
#     stock = relationship("Stock", back_populates="sales")

# # Создаем таблицы
# Base.metadata.create_all(engine)

# # Очистка существующих данных
# with Session(engine) as session:
#     session.query(Sale).delete()
#     session.query(Stock).delete()
#     session.query(Book).delete()
#     session.query(Shop).delete()
#     session.query(Publisher).delete()
#     session.commit()

# # Пример использования с новыми данными
# with Session(engine) as session:
#     publisher = Publisher(name="Издательство А")
#     session.add(publisher)
#     session.commit()

#     book = Book(title="Книга 1", id_publisher=publisher.id)
#     session.add(book)
#     session.commit()

#     shop = Shop(name="Магазин 1")
#     session.add(shop)
#     session.commit()

#     stock = Stock(id_book=book.id, id_shop=shop.id, count=100)
#     session.add(stock)
#     session.commit()

#     sale = Sale(price=500, date_sale="2025-03-09", id_stock=stock.id, count=2)
#     session.add(sale)
#     session.commit()

#     publishers = session.query(Publisher).all()
#     for p in publishers:
#         print(f"Издатель: {p.name}, Книги: {[book.title for book in p.books]}")

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy.sql import text  # Добавляем импорт для text()
from dotenv import load_dotenv
import os
from datetime import datetime

# Загружаем переменные из .env файла
load_dotenv()

# Получаем параметры подключения из переменных окружения
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

# Формируем строку подключения
connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string, echo=True)

# Создаем базовый класс для моделей
Base = declarative_base()

# Определяем модели
class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("Book", back_populates="publisher")

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)
    publisher = relationship("Publisher", back_populates="books")
    stocks = relationship("Stock", back_populates="book")

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stocks = relationship("Stock", back_populates="shop")

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False)
    book = relationship("Book", back_populates="stocks")
    shop = relationship("Shop", back_populates="stocks")
    sales = relationship("Sale", back_populates="stock")

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    date_sale = Column(Date, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=False)
    stock = relationship("Stock", back_populates="sales")

# Создаем таблицы
Base.metadata.create_all(engine)

# Очистка существующих данных
with Session(engine) as session:
    session.query(Sale).delete()
    session.query(Stock).delete()
    session.query(Book).delete()
    session.query(Shop).delete()
    session.query(Publisher).delete()
    session.commit()

# Сбрасываем последовательности id после очистки
with engine.connect() as connection:
    # Используем text() для выполнения сырых SQL-запросов
    connection.execute(text("ALTER SEQUENCE publisher_id_seq RESTART WITH 1;"))
    connection.execute(text("ALTER SEQUENCE book_id_seq RESTART WITH 1;"))
    connection.execute(text("ALTER SEQUENCE shop_id_seq RESTART WITH 1;"))
    connection.execute(text("ALTER SEQUENCE stock_id_seq RESTART WITH 1;"))
    connection.execute(text("ALTER SEQUENCE sale_id_seq RESTART WITH 1;"))
    connection.commit()

# Добавление тестовых данных
with Session(engine) as session:
    # Издатели
    publisher1 = Publisher(name="Пушкин")
    publisher2 = Publisher(name="Издательство А")
    session.add_all([publisher1, publisher2])
    session.commit()

    # Книги
    book1 = Book(title="Золотая рыбка", id_publisher=publisher1.id)
    book2 = Book(title="Евгений Онегин", id_publisher=publisher1.id)
    book3 = Book(title="Капитанская дочка", id_publisher=publisher1.id)
    book4 = Book(title="Книга 1", id_publisher=publisher2.id)
    session.add_all([book1, book2, book3, book4])
    session.commit()

    # Магазины
    shop1 = Shop(name="Буквоед")
    shop2 = Shop(name="Лабиринт")
    shop3 = Shop(name="Книжный дом")
    shop4 = Shop(name="Магазин 1")
    session.add_all([shop1, shop2, shop3, shop4])
    session.commit()

    # Запасы
    stock1 = Stock(id_book=book1.id, id_shop=shop1.id, count=100)
    stock2 = Stock(id_book=book1.id, id_shop=shop2.id, count=50)
    stock3 = Stock(id_book=book2.id, id_shop=shop3.id, count=30)
    stock4 = Stock(id_book=book3.id, id_shop=shop1.id, count=20)
    stock5 = Stock(id_book=book4.id, id_shop=shop4.id, count=100)
    session.add_all([stock1, stock2, stock3, stock4, stock5])
    session.commit()

    # Продажи
    sale1 = Sale(price=600, date_sale=datetime.strptime("2022-11-09", "%Y-%m-%d"), id_stock=stock1.id, count=2)
    sale2 = Sale(price=580, date_sale=datetime.strptime("2022-11-05", "%Y-%m-%d"), id_stock=stock2.id, count=1)
    sale3 = Sale(price=499, date_sale=datetime.strptime("2022-11-21", "%Y-%m-%d"), id_stock=stock3.id, count=1)
    sale4 = Sale(price=600, date_sale=datetime.strptime("2022-10-26", "%Y-%m-%d"), id_stock=stock4.id, count=3)
    sale5 = Sale(price=500, date_sale=datetime.strptime("2025-03-09", "%Y-%m-%d"), id_stock=stock5.id, count=2)
    session.add_all([sale1, sale2, sale3, sale4, sale5])
    session.commit()

# Вывод доступных издателей для помощи пользователю
with Session(engine) as session:
    publishers = session.query(Publisher).all()
    print("Доступные издатели:")
    for p in publishers:
        print(f"ID: {p.id}, Имя: {p.name}")

# Запрос имени или id издателя
publisher_input = input("Введите имя или id издателя: ")

# Выборка фактов покупки книг указанного издателя
with Session(engine) as session:
    # Проверяем, является ли ввод числом (id) или строкой (имя)
    try:
        publisher_id = int(publisher_input)
        publisher = session.query(Publisher).filter(Publisher.id == publisher_id).first()
    except ValueError:
        publisher = session.query(Publisher).filter(Publisher.name == publisher_input).first()

    if not publisher:
        print(f"Издатель '{publisher_input}' не найден.")
    else:
        # Запрос: находим все продажи книг указанного издателя
        sales = (session.query(Book, Shop, Sale)
                 .join(Stock, Book.id == Stock.id_book)
                 .join(Sale, Sale.id_stock == Stock.id)
                 .join(Shop, Stock.id_shop == Shop.id)
                 .filter(Book.id_publisher == publisher.id)
                 .all())

        # Вывод заголовка таблицы
        print("Название книги | Название магазина | Стоимость покупки | Дата покупки")
        print("-" * 70)

        # Вывод данных
        for book, shop, sale in sales:
            print(f"{book.title} | {shop.name} | {int(sale.price)} | {sale.date_sale.strftime('%d-%m-%Y')}")