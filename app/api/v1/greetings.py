from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.greeting import GreetingCreate, GreetingResponse
from app.services.greeting_service import GreetingService
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=GreetingResponse)
async def create_greeting(greeting_in: GreetingCreate, db: AsyncSession = Depends(get_db)):
    service = GreetingService(db)
    greeting = await service.create_greeting(
        sender_name=greeting_in.sender_name,
        recipient_name=greeting_in.recipient_name,
        message=greeting_in.message
    )
    return greeting

@router.get("/{token}", response_model=GreetingResponse)
async def get_greeting(token: str, db: AsyncSession = Depends(get_db)):
    service = GreetingService(db)
    greeting = await service.get_greeting_by_token(token)
    if not greeting:
        raise HTTPException(status_code=404, detail="Greeting not found")
    return greeting
