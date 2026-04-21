from fastapi import FastAPI, Depends, HTTPException,BackgroundTasks,Response
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database.database import engine,Base,get_db, AsyncSession
from .schema.user import MessageCreate,UserCreate,UserLogin
from .schema.blog import BlogCreate,BlogUpdate
from .schema.service import SeviceCreate,serviceUpdate
from .services.user import UserService
from .services.auth import AuthService,send_email_background
from .services.blog import BlogService
from .services.service import webService
from .core.config import settings
from .core.security import ALGORITHM,create_access_token
from jose import jwt,JWTError
from datetime import timedelta

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield 
    await engine.dispose()
    
app = FastAPI(debug=True,lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return {"message": "welcome to AshaTech"}

# ------------------------------------------Register user-------------------------------------------------

@app.post("/register", tags=["Auth"])
async def create_user(user_input: UserCreate, db: AsyncSession = Depends(get_db)): 
    user_service= UserService(db)
    await user_service.create_user(user_input)
    return {
        "Message":"User is created successfully"
    }
    
# ------------------------------------------login user----------------------------------------------------

@app.post("/login", tags=["Auth"])
async def login_user(user_input:UserLogin, response:Response ,db: AsyncSession =Depends(get_db)):
    auth_service= AuthService(db)
    token_data  = await auth_service.login_user(user_input)
    response.set_cookie(
        key="access_token",
        value=token_data,
        httponly=True,     
        secure=True,
        samesite="lax"
    )
    return {
        "message" : token_data
        }

# --------------------------------------refresh access token----------------------------------------------

@app.post("/refresh", tags=["Auth"])
def refresh_access_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    
    refresh_access= credentials.credentials
    
    try:
        payload = jwt.decode(refresh_access, settings.SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=403, detail="Invalid token type")
        
        user_id =payload.get("sub")
        
    except JWTError:
        raise HTTPException(
            status_code=403, detail="Invalid or expired refresh token"
        )
    new_access_token = create_access_token(
    data={"sub": user_id, "type": "access"},
    expire_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
)
    
    return {
        "access token": new_access_token,
        "token_type": "bearer"
    }

# ------------------------------------------Logged out user-----------------------------------------------

@app.post("/logout", tags=["Auth"])
def logout():
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie("access_token")
    return response

# -------------------------------------send email message from a form-------------------------------------

@app.post("/sendmessage", tags=["Auth"])
async def send_message(user_input: MessageCreate,bg: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    user_message = user_input
    if not user_message:
        raise HTTPException(status_code=404, detail={"message": "message not found"})
    bg.add_task(send_email_background, user_input)
    return {"message":"message sent successfully"}

# ------------------------------------------Create blog---------------------------------------------------

@app.post("/blog", tags=["Blogs"])
async def create_blog(user_input:BlogCreate,db:AsyncSession = Depends(get_db)):
    blog_service = BlogService(db)
    await blog_service.create_blog(user_input)
    return {
        "message" : "Blog is created"
    }
    
# ------------------------------------------Get blog Data-------------------------------------------------

@app.get("/{blog_id}", tags=["Blogs"])
async def get_blog(db: AsyncSession = Depends(get_db)):
    blog_service = BlogService(db)
    blog = await blog_service.get_blog()
    return blog

# ------------------------------------------Get first blog Data-------------------------------------------

@app.get("/blogs/{blog_id}", tags=["Blogs"])
async def get_blog_by_id(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog_service = BlogService(db)
    blog = await blog_service.get_blog_by_id(blog_id)
    if not blog:
        return {"message": "Blog not found"}
    return blog

# --------------------------------------------Update blog Data--------------------------------------------

@app.put("/{blog_id}", tags=["Blogs"])
async def update_blog(blog_id: int,user_input: BlogUpdate , db:AsyncSession = Depends(get_db)):
    blog_service = BlogService(db)
    result = await blog_service.update_blog(blog_id,user_input)
    return result

# --------------------------------------------Delete blog ------------------------------------------------

@app.delete("/{blog_id}", tags=["Blogs"])
async def delete_blog(blog_id:int, db: AsyncSession = Depends(get_db)):
    blog_service = BlogService(db)
    return await blog_service.delete_blog(blog_id)

# -------------------------------------- Create Service --------------------------------------

@app.post("/service", tags=["Service"])
async def create_service(user_input: SeviceCreate, db: AsyncSession = Depends(get_db)):
    service = webService(db)
    return await service.create_service(user_input)


# -------------------------------------- Get All Services ------------------------------------

@app.get("/service", tags=["Service"])
async def get_services(db: AsyncSession = Depends(get_db)):
    service = webService(db)
    return await service.get_service()


# -------------------------------------- First Service by ID -----------------------------------

@app.get("/service/{service_id}", tags=["Service"])
async def get_service_by_id(service_id: int, db: AsyncSession = Depends(get_db)):
    service = webService(db)
    blog = await service.get_service_by_id(service_id)
    if not blog:
        return {"message": "Service not found"}
    return blog

# -------------------------------------- Update Service --------------------------------------

@app.put("/service/{service_id}", tags=["Service"])
async def update_service(service_id: int, user_input: serviceUpdate, db: AsyncSession = Depends(get_db)):
    service = webService(db)
    return await service.update_service(service_id, user_input)


# -------------------------------------- Delete Service --------------------------------------

@app.delete("/service/{service_id}", tags=["Service"])
async def delete_service(service_id: int, db: AsyncSession = Depends(get_db)):
    service = webService(db)
    return await service.delete_service(service_id)