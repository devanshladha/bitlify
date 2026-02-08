from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from .. import schemas, database, models, auth
import os

router = APIRouter(tags = ['Authanticator'])

FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN")

config = Config('.env')
oauth = OAuth(config)

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# ----- FOR EMAIL AND PASSWORD SIGN UP -----

@router.post("/register", response_model=schemas.UserResponse)
async def register(user : schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    #1. check if user already exist in db
    result = await db.execute(select(models.User).where(models.User.email == user.email))
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    #2. if user is not in db, create a new user
    hashed_pass = auth.get_password_hash(user.password)

    new_user = models.User(
        name = user.name,
        email = user.email,
        hashed_password = hashed_pass,
        provider = "local"
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return(new_user)

# ----- FOR EMAIL AND PASSWORD LOGIN -----

@router.post("/token", response_model = schemas.Token)
async def login_for_access_token(
    form_data : OAuth2PasswordRequestForm = Depends(), 
    db : AsyncSession = Depends(database.get_db)
):
    #1. find user in db
    result = await db.execute(select(models.User).where(models.User.email == form_data.username))
    user = result.scalars().first()

    #2. verify password
    if not user or not user.hashed_password or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token({"sub":user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ----- FOR GOOGLE LOGIN -----

@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

# ----- Google Callback -----

@router.get("/auth/callback", name = "auth_callback")
async def auth_callback(request: Request, db: AsyncSession = Depends(database.get_db)):
    try:
        #1. try to get token from google
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')

        if not user_info:
            raise HTTPException(status_code=400, detail="Google Auth Failed")
        
        email = user_info['email']
        print(user_info)             #remove that only for logging data

        # check user already exist
        result = await db.execute(select(models.User).where(models.User.email == email))
        user = result.scalars().first()

        # create new user if not exist
        if not user :
            user = models.User(
                name = user_info['given_name'],
                email = email,
                provider = "google",
                hashed_password = None
            )

            db.add(user)
            await db.commit()
            await db.refresh(user)
        
        # create a JWT for new login
        access_token = auth.create_access_token({"sub": user.email})

        frontend_url = f"{FRONTEND_DOMAIN}/oauth/callback?token={access_token}"

        return RedirectResponse(url=frontend_url)
    
    except Exception as e:
        print(f"Error: {e}") 
        raise HTTPException(status_code=400, detail="Login failed")