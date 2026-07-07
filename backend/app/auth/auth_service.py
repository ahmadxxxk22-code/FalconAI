from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.database.models import (
    User,
    Subscription,
    LoginSession
)

from app.database.crud import CRUD

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)

class AuthService:

    def __init__(self, db: Session):

        self.db = db

        self.crud = CRUD()

    def register(

        self,

        username: str,

        email: str,

        password: str,

        full_name: str = "",

        phone: str = "",

        country: str = ""

    ):

        if self.crud.get_user_by_email(

            self.db,

            email

        ):

            raise Exception("Email already exists")

        if self.crud.get_user_by_username(

            self.db,

            username

        ):

            raise Exception("Username already exists")

        user = self.crud.create_user(

            self.db,

            username=username,

            email=email,

            password=hash_password(password),

            full_name=full_name,

            phone=phone,

            country=country

        )

        expires = datetime.utcnow() + timedelta(days=7)

        self.crud.create_subscription(

            self.db,

            user_id=user.id,

            plan="FREE",

            expires_at=expires,

            active=True

        )

        return user
