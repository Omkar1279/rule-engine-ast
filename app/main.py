from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import router as api_router
from app.core.database import engine
from app.models import rule

app = FastAPI(title="Rule Engine API")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(rule.Base.metadata.create_all)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
