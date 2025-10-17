from fastapi import Depends, FastAPI
from models import Product
from database import session, engine
import database_model
from sqlalchemy.orm import Session


app = FastAPI()

database_model.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welcome to flutter development"
    
products = [
    Product(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
    Product(id=2, name="Smartphone", description="A latest model smartphone", price=699.99, quantity=25),
    Product(id=3, name="Headphones", description="Noise-cancelling headphones", price=199.99, quantity=15),
    Product(id=6, name="Headphones", description="Noise-cancelling headphones", price=199.99, quantity=15),
]


def get_db():
    db = session()
    try:
        yield db 
    finally:
        # Ensure the database session is properly closed after each request
        db.close()


def init_db():
    db = session()
    count = db.query(database_model.Product).count()
    if count == 0:
        for i in products:
            db.add(database_model.Product(**i.model_dump()))
        db.commit()
init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_model.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        return db_product
    else: 
        return "product not found"

@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    product = database_model.Product(**product.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.put("/product")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.quantity = product.quantity
        db_product.price = product.price
        db.commit()
        return "Product updated"
    else:
        return "No products found"


@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]

    return "Product not found"
