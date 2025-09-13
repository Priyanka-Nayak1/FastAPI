from fastapi import FastAPI
from routes.employee_routes import router as employee_router
from routes.auth_routes import router as auth_router
from config.db import init_indexes

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_indexes()   # creates the index when app starts

# include employee routes
app.include_router(employee_router, prefix="/employees", tags=["Employees"])

# include auth routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

