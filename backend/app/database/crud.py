from sqlalchemy.orm import Session

from app.database.models import (
User,
Subscription,
SignalHistory,
LoginSession,
ApiKey
)

class CRUD:

# ==========================  
# Users  
# ==========================  

@staticmethod  
def create_user(  
    db: Session,  
    **kwargs  
):  

    user = User(**kwargs)  

    db.add(user)  

    db.commit()  

    db.refresh(user)  

    return user  

@staticmethod  
def get_user_by_email(  
    db: Session,  
    email: str  
):  

    return db.query(User).filter(  
        User.email == email  
    ).first()  

@staticmethod  
def get_user_by_username(  
    db: Session,  
    username: str  
):  

    return db.query(User).filter(  
        User.username == username  
    ).first()  

@staticmethod  
def get_user(  
    db: Session,  
    user_id: int  
):  

    return db.query(User).filter(  
        User.id == user_id  
    ).first()  

@staticmethod  
def update_user(  
    db: Session,  
    user: User  
):  

    db.commit()  

    db.refresh(user)  

    return user  

# ==========================  
# Subscription  
# ==========================  

@staticmethod  
def create_subscription(  
    db: Session,  
    **kwargs  
):  

    sub = Subscription(**kwargs)  

    db.add(sub)  

    db.commit()  

    db.refresh(sub)  

    return sub  

@staticmethod  
def get_subscription(  
    db: Session,  
    user_id: int  
):  

    return db.query(  
        Subscription  
    ).filter(  
        Subscription.user_id == user_id  
    ).first()  

# ==========================  
# Signal History  
# ==========================  

@staticmethod  
def save_signal(  
    db: Session,  
    **kwargs  
):  

    signal = SignalHistory(**kwargs)  

    db.add(signal)  

    db.commit()  

    db.refresh(signal)  

    return signal  

@staticmethod  
def get_signals(  
    db: Session,  
    user_id: int  
):  

    return db.query(  
        SignalHistory  
    ).filter(  
        SignalHistory.user_id == user_id  
    ).all()  

# ==========================  
# Login Sessions  
# ==========================  

@staticmethod  
def create_session(  
    db: Session,  
    **kwargs  
):  

    session = LoginSession(**kwargs)  

    db.add(session)  

    db.commit()  

    db.refresh(session)  

    return session  

# ==========================  
# API Keys  
# ==========================  

@staticmethod  
def save_api_key(  
    db: Session,  
    **kwargs  
):  

    api = ApiKey(**kwargs)  

    db.add(api)  

    db.commit()  

    db.refresh(api)  

    return api  

@staticmethod  
def get_api_keys(  
    db: Session,  
    user_id: int  
):  

    return db.query(  
        ApiKey  
    ).filter(  
        ApiKey.user_id == user_id  
    ).all()
