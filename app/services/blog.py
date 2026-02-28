from sqlalchemy.ext.asyncio import AsyncSession
from ..schema.blog import BlogCreate
from ..model.model import Blog

class BlogService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
    
    async def create_blog(self,user_input:BlogCreate):
        blog_create = Blog(**user_input.model_dump())
        self.db.add(blog_create)
        await self.db.commit()
        await self.db.refresh(blog_create)
        return blog_create