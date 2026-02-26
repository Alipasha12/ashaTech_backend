from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException,BackgroundTasks
from .database.database import engine,Base,get_db, AsyncSession
from .schema.user import MessageCreate,UserCreate
from .services.user import UserService
from .model.model import User
from email.mime.text import MIMEText
from .core.config import settings
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
    return {"welcome to AshaTech"}

# ------------------------------------------Register user-------------------------------------------------

@app.post("/register")
async def create_user(user_input: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service= UserService(db)
    await user_service.create_user(user_input)
    return {
        "Message":"User is created successfully"
    }


# -------------------------------------send email message from a form-------------------------------------------------

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
    # user_service= UserService(db)
    # await user_service.create_message(user_input)
    user_message = user_input
    if not user_message:
        raise HTTPException(status_code=404, detail={"message": "message not found"})
    bg.add_task(send_email_background, user_input)
    return {"message":"message sent successfully"}

