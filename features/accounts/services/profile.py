from django.contrib.auth import get_user_model

from core.services import BaseCRUDService
from features.accounts.models import Role, UserProfile

User = get_user_model()


class UserProfileService(BaseCRUDService[UserProfile]):
    model = UserProfile

    def get_user_role(self, user) -> str:
        profile = getattr(user, "profile", None)
        if profile:
            return profile.role
        if user.is_superuser:
            return Role.ADMIN
        return Role.RECRUITER

    def ensure_profile(self, user, role: str = Role.RECRUITER) -> UserProfile:
        profile = self.get_or_none_by_user(user)
        if profile:
            if profile.role != role:
                return self.update(profile, role=role)
            return profile
        return self.create(user=user, role=role)

    def get_or_none_by_user(self, user) -> UserProfile | None:
        return self.list(user=user).first()


profile_service = UserProfileService()
