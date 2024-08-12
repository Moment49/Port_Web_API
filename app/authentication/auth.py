from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas import schemas
from ..models import models
from . import token_gen
from ..database import Base, engine, SessionLocal, get_db
from jose import jwt
from ..Hashing import hashing


SECRET_KEY = "78YE7FGYWEI7F3RUCFEG78D6EFWEUEFW8OE"
ALGORITHM = "HS256"

router = APIRouter(
    tags=['Authentication']
)


@router.post('/admin', response_model=schemas.ShowAdmin, status_code=status.HTTP_201_CREATED)
def create_admin(request:schemas.CreateAdmin, db:Session = Depends(get_db)):
    admin_users = db.query(models.AdminUser).all()
    if admin_users:
       for admin_user in admin_users:
            if admin_user.email == request.email:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='ADMIN ALREADY EXISTS')

    # Hashing the password
    hashed_password = hashing.Hash.bcrypt(request.password)
    new_admin_user = models.AdminUser(fullname=request.fullname, email=request.email, password=hashed_password)
    db.add(new_admin_user)
    db.commit()
    db.refresh(new_admin_user) 

    return new_admin_user

@router.post('/login')
def admin_login(request:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    #query the database
    admin_user = db.query(models.AdminUser).filter(models.AdminUser.email == request.username).first()
    # check if user exists else raise the expections
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Username")
    
    # Verify the hash password
    if not hashing.Hash.verify(request.password, admin_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password")
    
    # Generate the JWT Token
    access_token = token_gen.create_access_token(
        payload={"admin_id": admin_user.id})
    return {'access_token':access_token, 'token_type':"bearer"}