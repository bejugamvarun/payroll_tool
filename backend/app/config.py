from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    APP_NAME: str = "Aurora Group Payroll Management"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://payroll_user:payroll_pass@localhost:5432/payroll_db"

    # Storage
    STORAGE_PATH: str = "storage"
    UPLOAD_PATH: str = "storage/uploads"
    PAYSLIP_PATH: str = "storage/payslips"
    REPORT_PATH: str = "storage/reports"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 200

    # CORS
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]

    # Leave Configuration
    DEFAULT_PAID_LEAVES_PER_YEAR: int = 12
    DEFAULT_MAX_CARRY_FORWARD: int = 5

    # Salary Calculation
    ANNUAL_MONTHS: int = 12
    WEEKEND_DAYS: list = [5, 6]  # Saturday=5, Sunday=6 (0=Monday)

    # Security (for future use)
    SECRET_KEY: str = "aurora-payroll-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
