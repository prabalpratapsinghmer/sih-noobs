"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="SIH26184", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # PostgreSQL
    postgres_url: str = Field(default="", alias="POSTGRES_URL")
    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    postgres_user: str = Field(default="sih_admin", alias="POSTGRES_USER")
    postgres_password: str = Field(default="password", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="sih26184_app", alias="POSTGRES_DB")
    pg_encryption_key: str = Field(
        default="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
        alias="PG_ENCRYPTION_KEY",
    )

    @property
    def sync_database_url(self) -> str:
        """Generate synchronous PostgreSQL URL for Alembic migrations."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # Neo4j
    neo4j_uri: str = Field(default="bolt://localhost:7687", alias="NEO4J_URI")
    neo4j_http_uri: str = Field(default="http://localhost:7474", alias="NEO4J_HTTP_URI")
    neo4j_user: str = Field(default="neo4j", alias="NEO4J_USER")
    neo4j_password: str = Field(default="password", alias="NEO4J_PASSWORD")

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")

    # JWT
    jwt_secret_key: str = Field(
        default="your-super-secret-key-change-in-production-min-64-chars-long!",
        alias="JWT_SECRET_KEY",
    )
    jwt_access_token_expire_minutes: int = Field(default=1440, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_days: int = Field(default=7, alias="JWT_REFRESH_TOKEN_EXPIRE_DAYS")

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        alias="CORS_ORIGINS",
    )

    # Rate Limiting
    rate_limit_per_user: int = Field(default=100, alias="RATE_LIMIT_PER_USER")
    rate_limit_per_ip: int = Field(default=1000, alias="RATE_LIMIT_PER_IP")

    # External Services (mock in dev)
    pinata_api_key: str = Field(default="mock_key", alias="PINATA_API_KEY")
    pinata_api_secret: str = Field(default="mock_secret", alias="PINATA_API_SECRET")
    whatsapp_api_token: str = Field(default="mock_token", alias="WHATSAPP_API_TOKEN")
    whatsapp_phone_number_id: str = Field(default="mock_number_id", alias="WHATSAPP_PHONE_NUMBER_ID")
    whatsapp_webhook_verify_token: str = Field(default="verify_token_here", alias="WHATSAPP_WEBHOOK_VERIFY_TOKEN")
    sendgrid_api_key: str = Field(default="mock_key", alias="SENDGRID_API_KEY")
    twilio_account_sid: str = Field(default="mock_sid", alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = Field(default="mock_token", alias="TWILIO_AUTH_TOKEN")
    twilio_phone_number: str = Field(default="+1234567890", alias="TWILIO_PHONE_NUMBER")

    # Celery
    celery_broker_url: str = Field(default="redis://localhost:6379/1", alias="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default="redis://localhost:6379/2", alias="CELERY_RESULT_BACKEND")

    # Supabase (Dual-Mode Cloud / Realtime / Storage)
    supabase_url: str = Field(default="", alias="SUPABASE_URL")
    supabase_key: str = Field(default="", alias="SUPABASE_KEY")
    supabase_service_role_key: str = Field(default="", alias="SUPABASE_SERVICE_ROLE_KEY")
    supabase_storage_bucket: str = Field(default="evidence", alias="SUPABASE_STORAGE_BUCKET")

    # Qdrant Vector Database
    qdrant_host: str = Field(default="localhost", alias="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, alias="QDRANT_PORT")
    qdrant_api_key: str = Field(default="", alias="QDRANT_API_KEY")
    qdrant_collection: str = Field(default="cybercrime_complaints", alias="QDRANT_COLLECTION")

    # Local / Free LLM (Ollama / vLLM)
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3", alias="OLLAMA_MODEL")

    # Deployed ATM prediction service. This must be a reachable service URL in production.
    model_api_url: str = Field(default="http://localhost:8001", alias="MODEL_API_URL")

    # OpenTelemetry & Tracing
    otel_service_name: str = Field(default="sih26184-backend", alias="OTEL_SERVICE_NAME")
    otel_exporter_otlp_endpoint: str = Field(default="http://localhost:4318", alias="OTEL_EXPORTER_OTLP_ENDPOINT")
    tracing_enabled: bool = Field(default=True, alias="TRACING_ENABLED")

    # High-Performance Caching
    cache_prediction_ttl: int = Field(default=300, alias="CACHE_PREDICTION_TTL")
    cache_mule_ttl: int = Field(default=300, alias="CACHE_MULE_TTL")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance (singleton pattern)."""
    return Settings()
