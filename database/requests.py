from sqlalchemy import select
from database.engine import async_session
from database.models import BookingModels


async def add_booking(user_id: int, service: str, name: str, phone: str, username: str | None = None):
    async with async_session() as session:
        session.add(BookingModels(
            user_id = user_id,
            service = service,
            name = name,
            phone = phone,
            username = username
        ))
        await session.commit()




async def get_user_bookings(user_id: int):
    async with async_session() as session:
        query = select(BookingModels).where(BookingModels.user_id == user_id)
        result = await session.execute(query)

        return result.scalars().all()