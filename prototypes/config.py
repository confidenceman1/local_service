import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """应用配置类"""
    
    # 阿里云百炼 API
    DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")
    MODEL = os.environ.get("MODEL", "qwen-turbo")
    
    # PostgreSQL 数据库
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "local_service")
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    
    @classmethod
    def get_db_config(cls):
        return {
            'host': cls.DB_HOST,
            'port': cls.DB_PORT,
            'database': cls.DB_NAME,
            'user': cls.DB_USER,
            'password': cls.DB_PASSWORD
        }
