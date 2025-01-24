from sqlalchemy import Column, Integer, DateTime, String, Boolean, func

class Metadata:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())  
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  
    created_by = Column(String(50))  
    updated_by = Column(String(50))  
    is_deleted = Column(Boolean, default=False)
