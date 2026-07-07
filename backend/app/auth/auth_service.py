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
    def login(

        self,

        email: str,

        password: str,

        device: str = "Unknown",

        ip: str = "0.0.0.0"

    ):

        user = self.crud.get_user_by_email(

            self.db,

            email

        )

        if user is None:

            raise Exception("Invalid email or password")

        if not verify_password(

            password,

            user.password

        ):

            raise Exception("Invalid email or password")

        access_token = create_access_token(

            {
                "user_id": user.id,
                "email": user.email
            }

        )

        refresh_token = create_refresh_token(

            {
                "user_id": user.id
            }

        )

        self.crud.create_session(

            self.db,

            user_id=user.id,

            token=access_token,

            device=device,

            ip=ip

        )

        return {

            "user": user,

            "access_token": access_token,

            "refresh_token": refresh_token,

            "token_type": "bearer"

        }

    def get_user(

        self,

        user_id: int

    ):

        return self.crud.get_user(

            self.db,

            user_id

        )

    def verify_access_token(

        self,

        token: str

    ):

        from app.core.security import verify_token

        payload = verify_token(token)

        if payload is None:

            return None

        user_id = payload.get("user_id")

        if user_id is None:

            return None

        return self.crud.get_user(

            self.db,

            user_id

        )

    def logout(

        self,

        token: str

    ):

        session = self.db.query(

            LoginSession

        ).filter(

            LoginSession.token == token

        ).first()

        if session:

            self.db.delete(session)

            self.db.commit()

        return True
