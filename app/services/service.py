from sqlalchemy.ext.asyncio import AsyncSession
from ..schema.service import SeviceCreate,serviceUpdate
from ..model.model import Service
from sqlalchemy import select

class webService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
    
    async def create_service(self,user_input:SeviceCreate):
        service_create = Service(**user_input.model_dump())
        self.db.add(service_create)
        await self.db.commit()
        await self.db.refresh(service_create)
        return service_create
    
    async def get_service(self):
        result = await self.db.execute(select(Service))
        return result.scalars().all()
    
    async def get_service_by_id(self, Service_id :int):
        result = await self.db.execute(select(Service).where(Service.id == Service_id))
        return result.scalars().first()
    
    async def update_service(self,service_id:int,user_input:serviceUpdate):
        service = await self.get_service_by_id(service_id)
        
        if not service:
            return {"service is not found"}
        
        for key,value in user_input.model_dump(exclude_unset=True).items():
            setattr(service,key,value)
            
        await self.db.commit()
        await self.db.refresh(service)
        return service

    async def delete_service(self, service_id:int):
        service = await self.get_service_by_id(service_id)
        
        if not service:
            return {"service is not found"}
        
        await self.db.delete(service)
        await self.db.commit()
        return {"Message": "service is deleted successfully"}