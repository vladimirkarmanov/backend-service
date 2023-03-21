import os


class Config:
    DEBUG: bool = os.getenv('DEBUG', False)
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = os.getenv('PORT', 8000)
    DATABASE_URL: str = os.getenv('DATABASE_URL')
