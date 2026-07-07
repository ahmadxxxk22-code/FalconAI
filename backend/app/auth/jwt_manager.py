from datetime import datetime, timedelta

from jose import jwt, JWTError


SECRET_KEY = "CHANGE_THIS_SECRET_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


class JWTManager:

    @staticmethod
    def create_token(data: dict):

        payload = data.copy()

        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload["exp"] = expire

        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    @staticmethod
    def verify_token(token: str):

        try:

            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            return payload

        except JWTError:

            return None
