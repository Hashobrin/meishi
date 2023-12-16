from sqlalchemy.ext.asyncio import AsyncSession

import api.models.user as user_model
import api.schemas.main as main_schema


async def create_main(
        db: AsyncSession, user_create: main_schema.MainCreate
    ) -> user_model.User:
    user = user_model.User(**user_create.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
