# models/models.py
# Modelo ORM de la tabla 'stories' usando SQLAlchemy

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from config.database import Base
from datetime import datetime
import uuid


class Story(Base):
    __tablename__ = "stories"

    # 🔑 ID único de la historia (UUID en texto)
    id = Column(String, primary_key=True, index=True)

    # 👤 ID del perfil infantil asociado (por ahora texto libre)
    profile_id = Column(String, nullable=True)

    # 🔄 Estado de la historia: pending, generating, completed, failed
    status = Column(String, default="pending")

    # 🕒 Tiempos de creación y actualización
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 📁 Ruta absoluta o URL al archivo de video final
    video_path = Column(String, nullable=True)

    # ❌ Mensaje de error si la historia falla
    error_message = Column(Text, nullable=True)





class ChildProfile(Base):
    __tablename__ = "child_profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    avatar_url = Column(String, nullable=True)  # Puede ser ruta local o URL
    adulto_email = Column(String, nullable=False)  # Relacionado con JWT identity
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "edad": self.edad,
            "avatar_url": self.avatar_url,
            "adulto_email": self.adulto_email,
            "created_at": self.created_at.isoformat()
        }
