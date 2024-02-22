import logging
import threading
from configparser import ConfigParser
from pathlib import Path
from cryptography.fernet import Fernet


class PropertyManager:
    """
    Clase para gestionar propiedades desde un archivo de configuración.
    """

    logger = logging.getLogger(__name__)
    loader = Path(__file__).parent.parent  # Suponiendo la estructura de directorios
    PROPERTY_FILE_NAME = "config.properties"
    properties = threading.local()
    fernet_key = None

    def __init__(self):
        pass

    @classmethod
    def get_properties(cls):
        """Obtiene las propiedades cargadas, cargándolas si es necesario."""
        if cls.properties.properties is None:
            cls.load_properties()
        return cls.properties.properties

    @classmethod
    def is_properties_file_present(cls):
        """Comprueba si el archivo de propiedades está presente."""
        return cls.loader / cls.PROPERTY_FILE_NAME in Path().glob("**/config.properties")

    @classmethod
    def get_property(cls, property_key):
        """Obtiene el valor de una propiedad."""
        return cls.get_properties().get(property_key)

    @classmethod
    def is_property_present_and_not_empty(cls, property_key):
        """Comprueba si una propiedad está presente y no está vacía."""
        return property_key in cls.get_properties() and cls.get_properties().get(property_key)

    @classmethod
    def _decrypt_property(cls, encrypted_value):
        """Desencripta un valor de propiedad."""
        try:
            return Fernet(cls.fernet_key).decrypt(bytes(encrypted_value, "utf-8")).decode("utf-8")
        except Exception:
            return None

    @classmethod
    def load_properties(cls):
        """Carga las propiedades desde el archivo de configuración."""
        config = ConfigParser()
        path = cls.loader / cls.PROPERTY_FILE_NAME

        if path.is_file():
            try:
                config.read(path)
                cls.properties.properties = dict(config)
                for key, value in cls.properties.properties.items():
                    decrypted_value = cls._decrypt_property(value)
                    if decrypted_value is not None:
                        cls.properties.properties[key] = decrypted_value
            except Exception as e:
                cls.logger.error("Error al cargar el archivo de propiedades: %s", str(e))

    @classmethod
    def set_fernet_key(cls, fernet_key):
        """Establece la clave de Fernet para la encriptación/desencriptación."""
        cls.fernet_key = fernet_key
