# schemas_lib.py

# Definición del contrato para pedidos
PEDIDO_SCHEMA = {
    "type": "object",
    "properties": {
        "id_pedido": {"type": "number"},
        "cliente": {"type": "string", "minLength": 3},
        "productos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item": {"type": "string"},
                    "cantidad": {"type": "number", "minimum": 1}
                },
                "required": ["item", "cantidad"]
            }
        },
        "metodo_pago": {"type": "string", "enum": ["efectivo", "tarjeta"]},
        "total": {"type": "number", "minimum": 0}
    },
    "required": ["id_pedido", "cliente", "productos", "total", "metodo_pago"]
}

# Puedes centralizar otros esquemas aquí
USER_SCHEMA = { }
INVENTORY_SCHEMA = { }
