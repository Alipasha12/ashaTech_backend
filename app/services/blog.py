from sqlalchemy.ext.asyncio import AsyncSession
from ..schema.blog import BlogCreate,BlogUpdate
from ..model.model import Blog
from sqlalchemy import select

class BlogService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
    
    async def create_blog(self,user_input:BlogCreate):
        blog_create = Blog(**user_input.model_dump())
        self.db.add(blog_create)
        await self.db.commit()
        await self.db.refresh(blog_create)
        return blog_create
    
    async def get_blog(self):
        result = await self.db.execute(select(Blog))
        return result.scalars().all()
    
    async def get_blog_by_id(self, blog_id: int):
        result = await self.db.execute(select(Blog).where(Blog.id == blog_id))
        return result.scalars().first()
    
    async def update_blog(self, blog_id :int,user_input:BlogUpdate):
        blog = await self.get_blog_by_id(blog_id)
        
        if not blog:
            return {"blog is not found"}
        
        for key,value in user_input.model_dump(exclude_unset=True).items():
            setattr(blog , key , value)
        
        await self.db.commit()
        await self.db.refresh(blog)
        return blog
    
    
    async def delete_blog(self, blog_id:int):
        blog = await self.get_block_by_id(blog_id)
        
        if not blog:
            return {"blog is not founded"}
        
        await self.db.delete(blog)
        await self.db.commit()
        return {"Message": "Blog is deleted successfully"}