from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.profile.model import UserProfile


class UserProfileRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_by_user_id(
        self,
        user_id: int,
    ) -> UserProfile | None:
        return self.db.scalar(
            select(UserProfile).where(
                UserProfile.user_id == user_id,
            )
        )

    def create(
        self,
        profile: UserProfile,
    ) -> UserProfile:
        self.db.add(profile)
        self.db.flush()
        self.db.refresh(profile)

        return profile

    def update(
        self,
        profile: UserProfile,
    ) -> UserProfile:
        self.db.flush()
        self.db.refresh(profile)

        return profile

    def exists(
        self,
        user_id: int,
    ) -> bool:
        return (
            self.get_by_user_id(user_id)
            is not None
        )