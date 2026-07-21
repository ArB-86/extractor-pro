from fastapi import APIRouter

api_router = APIRouter(prefix="/api")


@api_router.get("/ping", tags=["System"])
async def ping() -> dict[str, str]:
    return {"message": "pong"}
