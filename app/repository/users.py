from sqlalchemy.orm import Session

from app.models import User


def get_user(db: Session, login: str):
    # Убрал print, в продакшене используют logging
    return db.query(User).filter(User.login == login).scalar()


def create_user(db: Session, login: str):
    user = User(login=login)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
