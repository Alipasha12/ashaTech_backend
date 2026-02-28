from fastapi import FastAPI, Depends, HTTPException,BackgroundTasks,Response
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from .database.database import engine,Base,get_db, AsyncSession
from .schema.user import MessageCreate,UserCreate,UserLogin
from .services.user import UserService
from .services.auth import AuthService
from .model.model import User
from email.mime.text import MIMEText
from .core.config import settings
from .core.security import ALGORITHM,create_access_token
from jose import jwt,JWTError
from datetime import timedelta
import smtplib

@asynccontextmanager
async def lifespan(app=FastAPI):
    async with engine.begin() as conn:
        
        table_exists = await conn.run_sync(
            lambda sync_conn: engine.dialect.has_table(sync_conn,User.__tablename__)
        )
        if not table_exists:
            await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    
    
app = FastAPI(debug=True,lifespan=lifespan)


@app.get("/")
def hello():
    return {"message": "welcome to AshaTech"}

# ------------------------------------------Register user-------------------------------------------------

@app.post("/register")
async def create_user(user_input: UserCreate, db: AsyncSession = Depends(get_db)): 
    user_service= UserService(db)
    await user_service.create_user(user_input)
    return {
        "Message":"User is created successfully"
    }
    
# ------------------------------------------login user--------------------------------------------

@app.post("/login")
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

# --------------------------------------refresh access token------------------------------------

@app.post("/refresh")
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

# ------------------------------------------Logged out user--------------------------------------

@app.post("/logout")
def logout():
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie("access_token")
    return response

# -------------------------------------send email message from a form----------------------------

def send_email_background(user_input: MessageCreate):
    body = f"""
    New Message Received

    Name: {user_input.name}
    Email: {user_input.email}
    Phone: {user_input.phone_no}

    Message:
    {user_input.message}
    """
    msg = MIMEText(body)
    msg["Subject"] = user_input.subject
    msg["From"] = user_input.email
    msg["To"] = settings.EMAIL_ADDRESS

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.send_message(msg)

@app.post("/sendmessage")
async def send_message(user_input: MessageCreate,bg: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    user_message = user_input
    if not user_message:
        raise HTTPException(status_code=404, detail={"message": "message not found"})
    bg.add_task(send_email_background, user_input)
    return {"message":"message sent successfully"}

