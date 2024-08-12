from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status


SECRET_KEY = "78YE7FGYWEI7F3RUCFEG78D6EFWEUEFW8OE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 35

security_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(payload: dict):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_timestamp = int(expire.timestamp())
    payload.update({"exp": expire_timestamp})
    encoded_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token



def get_verify_user_token(token:str = Depends(security_scheme)):
    # create the expection to handle when the user/token validation fails
    credentials_expections = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="could not validate credentials",
                                            headers={"WWW-Authenticate": "Bearer"}
                                            )
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        # admin_id:int = decoded_payload['username']
        admin_id: str = decoded_payload.get("admin_id")

        if admin_id is None:
            raise credentials_expections
    except JWTError:
        raise credentials_expections
    
    return admin_id
    