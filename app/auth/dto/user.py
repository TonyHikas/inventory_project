from pydantic import EmailStr, BaseModel, constr, validator


class UserRegisterDto(BaseModel):
    email: EmailStr
    phone: str | None
    first_name: constr(regex=r"^[a-zA-Zа-яА-Я,.'-]+$")
    password: constr(regex=r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=\S+$).{8,}$')
    password2: str

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    @validator('phone')
    def phone_format(cls, v: str, values, **kwargs):
        if v.isdigit() and 11 <= len(v) <= 14:
            return v
        raise ValueError('Phone format if not valid')
