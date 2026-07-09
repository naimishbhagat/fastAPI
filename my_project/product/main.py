from fastapi import FastAPI
from product import models
from database import engine
from routers import product, seller, login

app = FastAPI(
    title="Product API",
    description="This is a Product API built with FastAPI and SQLAlchemy.",
    version="1.0.0",    
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Naimish Bhagat",
        "url": "http://example.com/contact/",
        "email": "naimish_bhagat@yahoo.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

models.Base.metadata.create_all(bind=engine)

app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)

