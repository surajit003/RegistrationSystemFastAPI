from typing import Optional

import pydantic
from pydantic import BaseModel, validator
from validate_email import validate_email


class AllOptional(pydantic.main.ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        namespaces['__annotations__'] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str

    @validator('email')
    def validate_email(cls, value):
        is_valid = validate_email(value, check_format=True,
                                  check_blacklist=True,
                                  check_dns=True,
                                  dns_timeout=10,
                                  check_smtp=True,
                                  smtp_timeout=10,
                                  smtp_helo_host='my.host.name',
                                  smtp_from_address='my@from.addr.ess',
                                  smtp_skip_tls=False,
                                  smtp_tls_context=None,
                                  smtp_debug=False)
        if not is_valid:
            raise ValueError("Email is not Valid!")
        return value


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentPatch(StudentBase, metaclass=AllOptional):
    pass
