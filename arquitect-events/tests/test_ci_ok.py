import pytest

def test_config_env_vars():
    """Verifica que el sistema puede leer variables de entorno básicas"""
    import os
    # En el CI, podemos simular variables
    os.environ['APP_ENV'] = 'CI_TEST'
    assert os.getenv('APP_ENV') == 'CI_TEST'

def test_logic_addition():
    """Una prueba matemática simple para validar que pytest funciona"""
    assert 1 + 1 == 2