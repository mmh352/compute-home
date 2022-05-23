"""Setup functionality."""
from ..models import get_engine, Base


async def setup_database() -> None:
    """Create the database tables."""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
