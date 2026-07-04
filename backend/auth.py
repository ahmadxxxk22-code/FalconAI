from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext

from config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    data: dict,
    expires_minutes: int = None
):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(

        minutes=expires_minutes
        or settings.ACCESS_TOKEN_EXPIRE_MINUTES

    )

    to_encode.update({

        "exp": expire,

        "type": "access"

    })

    return jwt.encode(

        to_encode,

        settings.SECRET_KEY,

        algorithm=settings.ALGORITHM

    )


def decode_access_token(token: str):

    try:

        payload = jwt.decode(

            token,

            settings.SECRET_KEY,

            algorithms=[settings.ALGORITHM]

        )

        return payload

    except JWTError:

        return None


def token_is_valid(token: str):

    payload = decode_access_token(token)

    return payload is not None


def create_refresh_token(data: dict):

    expire = datetime.utcnow() + timedelta(days=30)

    payload = data.copy()

    payload.update({

        "exp": expire,

        "type": "refresh"

    })

    return jwt.encode(

        payload,

        settings.SECRET_KEY,

        algorithm=settings.ALGORITHM

    )
