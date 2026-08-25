from datetime import datetime, timedelta
import random
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "sqlite:///company.db"
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()


# ----------------------------------------------------------------------
# Models Definitions
# ----------------------------------------------------------------------
class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  email = Column(String, unique=True, nullable=False)
  city = Column(String)
  created_at = Column(DateTime, default=datetime.now)

  orders = relationship("Order", back_populates="user")
  reviews = relationship("Review", back_populates="user")


class Category(Base):
  __tablename__ = "categories"
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False, unique=True)

  products = relationship("Product", back_populates="category")


class Product(Base):
  __tablename__ = "products"
  id = Column(Integer, primary_key=True)
  category_id = Column(Integer, ForeignKey("categories.id"))
  title = Column(String, nullable=False)
  price = Column(Float, nullable=False)
  stock = Column(Integer, default=0)

  category = relationship("Category", back_populates="products")
  order_items = relationship("OrderItem", back_populates="product")
  reviews = relationship("Review", back_populates="product")


class Order(Base):
  __tablename__ = "orders"
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  total_amount = Column(Float, default=0.0)
  status = Column(String, default="Completed")  # Completed, Pending, Cancelled
  created_at = Column(DateTime, default=datetime.now)

  user = relationship("User", back_populates="orders")
  items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
  __tablename__ = "order_items"
  id = Column(Integer, primary_key=True)
  order_id = Column(Integer, ForeignKey("orders.id"))
  product_id = Column(Integer, ForeignKey("products.id"))
  quantity = Column(Integer, default=1)
  unit_price = Column(Float, nullable=False)

  order = relationship("Order", back_populates="items")
  product = relationship("Product", back_populates="order_items")


class Review(Base):
  __tablename__ = "reviews"
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  product_id = Column(Integer, ForeignKey("products.id"))
  rating = Column(Integer)  # 1 to 5
  comment = Column(Text)
  created_at = Column(DateTime, default=datetime.now)

  user = relationship("User", back_populates="reviews")
  product = relationship("Product", back_populates="reviews")


# ----------------------------------------------------------------------
# Data Initialization
# ----------------------------------------------------------------------
def init_db():
  Base.metadata.create_all(engine)
  Session = sessionmaker(bind=engine)
  session = Session()

  if session.query(User).count() == 0:
    cat_names = ["Electronics", "Furniture", "Books", "Clothing", "Appliances"]
    cats = [Category(name=c) for c in cat_names]
    session.add_all(cats)
    session.commit()

    products_data = [
        ("Laptop Pro 15", 1400.0, 15, cats[0]),
        ("Wireless Mouse", 25.0, 100, cats[0]),
        ("Mechanical Keyboard", 85.0, 40, cats[0]),
        ("4K Monitor 27", 350.0, 20, cats[0]),
        ("Ergonomic Chair", 250.0, 12, cats[1]),
        ("Standing Desk", 450.0, 8, cats[1]),
        ("Python Programming", 40.0, 50, cats[2]),
        ("SQL & Database Design", 35.0, 60, cats[2]),
        ("Cotton T-Shirt", 20.0, 200, cats[3]),
        ("Jeans Pants", 55.0, 80, cats[3]),
        ("Espresso Coffee Maker", 180.0, 15, cats[4]),
    ]
    products = [
        Product(title=t, price=p, stock=s, category=c)
        for t, p, s, c in products_data
    ]
    session.add_all(products)
    session.commit()

    users_data = [
        ("Ali Rezaei", "ali@example.com", "Tehran"),
        ("Sara Ahmadi", "sara@example.com", "Isfahan"),
        ("Mohammad Karimi", "m.karimi@example.com", "Shiraz"),
        ("Neda Ghasemi", "neda@example.com", "Mashhad"),
        ("Reza Golami", "reza@example.com", "Tabriz"),
        ("Maryam Hassani", "maryam@example.com", "Tehran"),
        ("Hossein Rahimi", "h.rahimi@example.com", "Karaj"),
        ("Zahra Kazemi", "zahra@example.com", "Isfahan"),
    ]
    users = [User(name=n, email=e, city=c) for n, e, c in users_data]
    session.add_all(users)
    session.commit()

    base_date = datetime.now() - timedelta(days=90)
    statuses = ["Completed", "Pending", "Cancelled"]

    for user in users:
      for _ in range(random.randint(2, 5)):
        order_date = base_date + timedelta(days=random.randint(1, 90))
        order = Order(
            user=user,
            status=random.choice(statuses),
            created_at=order_date,
            total_amount=0.0,
        )

        selected_products = random.sample(products, random.randint(1, 3))
        total = 0.0

        for prod in selected_products:
          qty = random.randint(1, 2)
          item = OrderItem(
              order=order, product=prod, quantity=qty, unit_price=prod.price
          )
          session.add(item)
          total += prod.price * qty

        order.total_amount = total
        session.add(order)

    comments = [
        "Great quality!",
        "A bit expensive.",
        "Highly recommended.",
        "Not bad, but could be better.",
        "Excellent product!",
    ]
    for _ in range(20):
      user = random.choice(users)
      prod = random.choice(products)
      review = Review(
          user=user,
          product=prod,
          rating=random.randint(1, 5),
          comment=random.choice(comments),
          created_at=base_date + timedelta(days=random.randint(1, 90)),
      )
      session.add(review)

    session.commit()

  session.close()


if __name__ == "__main__":
  init_db()
  print("Database created with 6 relational tables successfully!")