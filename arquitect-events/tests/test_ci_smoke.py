import pytest
import os
import sys

def test_python_environment():
    """Verifica que las librerías críticas están instaladas"""
    import stomp
    import jsonschema
    assert stomp.__version__ is not None
    assert jsonschema.__version__ is not None

def test_assets_presence():
    """Verifica que los archivos de datos existen en el contenedor"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_path = os.path.join(base_dir, 'assets')
    assert os.path.exists(assets_path), "La carpeta de assets no existe"
    assert len(os.listdir(assets_path)) > 0, "La carpeta de assets está vacía"

def test_env_variables():
    """Verifica que Docker inyectó las variables de configuración"""
    # En CI/CD estas variables deben estar definidas
    assert os.getenv('BROKER_HOST') is not None, "BROKER_HOST no definido"
    