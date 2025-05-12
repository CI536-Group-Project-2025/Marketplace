from fastapi import FastAPI
from routes import item, user, basket  # Adjust if your route files are under a different folder

app = FastAPI(title="Marketplace API")

# Register route modules
app.include_router(item.router, prefix="/item")
app.include_router(user.router, prefix="/user")
app.include_router(basket.router, prefix="/basket")

@app.get("/")
def root():
    return {"message": "Marketplace API running"}
