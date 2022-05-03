def convert_to_dict(obj: list):
    result = [item.as_dict() for item in obj]
    return result
