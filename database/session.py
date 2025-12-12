import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database.model import Base
from dotenv import load_dotenv

load_dotenv()


class DatabaseSession:
    """데이터베이스 세션 관리 싱글톤"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize(self):
        """데이터베이스 초기화"""
        if self._initialized:
            return
        
        db_path = os.getenv("DB_PATH", "content_history.db")
        db_url = f"sqlite:///{db_path}"
        
        # 엔진 생성
        self.engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False}  # SQLite용
        )
        
        # 테이블 생성
        Base.metadata.create_all(self.engine)
        
        # 세션 팩토리 생성
        session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)
        
        self._initialized = True
    
    def get_session(self):
        """세션 반환"""
        if not self._initialized:
            self.initialize()
        return self.Session()
    
    def close(self):
        """세션 정리"""
        if self._initialized and hasattr(self, 'Session'):
            self.Session.remove()


# 전역 인스턴스
db_session = DatabaseSession()
