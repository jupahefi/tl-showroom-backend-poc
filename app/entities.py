import enum
from datetime import datetime
from typing import Optional, List


class ProfileStatus(enum.Enum):
    """
    Enum representing the status of a profile.
    Used throughout the application to ensure consistency.
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class Profile:
    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        email: str = "",
        specialty: str = "",
        linkedin: Optional[str] = None,
        status: ProfileStatus = ProfileStatus.ACTIVE,
        start_date: datetime = None,
        end_date: Optional[datetime] = None,
        history: List["ProfileHistory"] = None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.specialty = specialty
        self.linkedin = linkedin
        self.status = status
        self.start_date = start_date or datetime.utcnow()
        self.end_date = end_date
        self.history = history or []


class ProfileHistory:
    def __init__(
        self,
        id: Optional[int] = None,
        profile_id: int = None,
        status: ProfileStatus = None,
        changed_at: datetime = None,
        profile: Optional[Profile] = None,
    ):
        self.id = id
        self.profile_id = profile_id
        self.status = status
        self.changed_at = changed_at or datetime.utcnow()
        self.profile = profile