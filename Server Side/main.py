from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datafetcher import router as datafetcher_router
from auth import router as auth_router
from database import engine, Base

# Import models to ensure they are registered with Base
import models  

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend access
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(auth_router)
app.include_router(datafetcher_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
