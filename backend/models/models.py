# models/models.py

from datetime import datetime

class Story:
    """
    Clase Story que representa una historia generada por Cuentix.
    Cada instancia contiene los datos necesarios para seguir el estado y el archivo generado.
    """

    def __init__(self, id, profile_id, status="pending", created_at=None, updated_at=None, video_path=None):
        """
        Inicializa una nueva instancia de Story.

        Args:
            id (str): ID único de la historia.
            profile_id (str): ID del perfil infantil que solicitó la historia.
            status (str, optional): Estado de la historia ('pending', 'generating', 'completed', 'failed'). Default 'pending'.
            created_at (datetime, optional): Momento de creación. Default: ahora mismo.
            updated_at (datetime, optional): Última actualización. Default: ahora mismo.
            video_path (str, optional): Ruta al video generado cuando esté listo.
        """
        self.id = id
        self.profile_id = profile_id
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.video_path = video_path  # Ruta al archivo final de video

    def to_dict(self):
        """
        Serializa la historia a un diccionario, para responder en APIs o guardar.

        Returns:
            dict: Representación en diccionario de la historia.
        """
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "video_path": self.video_path
        }

    def update_status(self, new_status, video_path=None):
        """
        Actualiza el estado de la historia.

        Args:
            new_status (str): Nuevo estado ('generating', 'completed', 'failed').
            video_path (str, optional): Ruta al video final si aplica.
        """
        self.status = new_status
        self.updated_at = datetime.utcnow()
        if video_path:
            self.video_path = video_path

