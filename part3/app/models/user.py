import re
from app.models.base_model import BaseModel
from app import db, bcrypt


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email      = db.Column(db.String(120), nullable=False, unique=True)
    password   = db.Column(db.String(128), nullable=False)
    is_admin   = db.Column(db.Boolean, default=False)

    def __init__(self, first_name: str = '', last_name: str = '',
                 email: str = '', is_admin: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.first_name = self._validate_name(first_name, 'first_name')
        self.last_name  = self._validate_name(last_name,  'last_name')
        self.email      = self._validate_email(email)
        self.is_admin   = bool(is_admin)

    # ── Validators ────────────────────────────────────────────────────────
    @staticmethod
    def _validate_name(value: str, field: str) -> str:
        if not value or len(value) > 50:
            raise ValueError(f"{field} must be between 1 and 50 characters.")
        return value

    @staticmethod
    def _validate_email(email: str) -> str:
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValueError("Invalid email address.")
        return email

    # ── Password ──────────────────────────────────────────────────────────
    def hash_password(self, password: str):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    # ── Serialisation ─────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            'first_name': self.first_name,
            'last_name':  self.last_name,
            'email':      self.email,
            'is_admin':   self.is_admin,
        })
        return base