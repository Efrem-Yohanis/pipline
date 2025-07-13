# executors/utils.py

def load_subnode_config(subnode):
    params = subnode.parameters.all()
    config = {}
    for param in params:
        key = param.key.upper()
        value = param.value
        if param.value_type == "integer":
            value = int(value)
        elif param.value_type == "boolean":
            value = value.lower() in ("yes", "true", "1")
        config[key] = value
    return config
