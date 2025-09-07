from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from .routers import chart, order, signal, backtest
from .middleware.auth import verify_token
from .config.settings import settings

app = FastAPI(title="AI-Tradingview-Core API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme
security = HTTPBearer()

# Include routers
app.include_router(chart.router, prefix="/api/chart", tags=["chart"])
app.include_router(order.router, prefix="/api/order", tags=["order"], dependencies=[Depends(verify_token)])
app.include_router(signal.router, prefix="/api/signal", tags=["signal"])
app.include_router(backtest.router, prefix="/api/backtest", tags=["backtest"])

@app.get("/")
async def root():
    return {"message": "AI-Tradingview-Core API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)