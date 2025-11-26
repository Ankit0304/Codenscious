from fastapi import FastAPI, Depends
from models import *
from database import session, engine
import database_model
from sqlalchemy.orm import Session

app = FastAPI()

database_model.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"WElCOME TO FAST API"}

products = [
    Products(id=1, name="Laptop", description="A high performance laptop", price=999.99, quantity=10),
    Products(id=2, name="Smartphone", description="A latest model smartphone", price=699.99, quantity=25),
    Products(id=3, name="Headphones", description="Noise cancelling headphones", price=199.99, quantity=50), 
    Products(id=4, name="Monitor", description="4K UHD Monitor", price=399.99, quantity=15),
    Products(id=5, name="Keyboard", description="Mechanical keyboard", price=89.99, quantity=30)
]   

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_model.Products).count()
    if count == 0:
        for product in products:
            db.add(database_model.Products(**product.model_dump()))
        db.commit()

init_db()


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(database_model.Products).all()
    return db_products 

@app.get("/products/{id}")
def get_product_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Products).filter(database_model.Products.id == id).first()
    if db_product:
        return db_product
    return {"error": "Product not found"}

@app.post("/products")
def add_product(product: Products, db: Session = Depends(get_db)):
    db.add(database_model.Products(**product.model_dump()))
    db.commit()
    return {"message": "Product added successfully"}

@app.put('/products')
def update_product(id :int, updated_product: Products, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Products).filter(database_model.Products.id == id).first()
    if db_product:
        db_product.name = updated_product.name
        db_product.description = updated_product.description
        db_product.price = updated_product.price
        db_product.quantity = updated_product.quantity
        db.commit()
        return {"message": "Product updated successfully"}
    return {"error": "Product not found"}

@app.delete('/products/{id}')
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Products).filter(database_model.Products.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    return {"error": "Product not found"}
