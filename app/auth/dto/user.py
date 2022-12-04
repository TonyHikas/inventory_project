from pydantic import EmailStr, BaseModel, constr, validator


class UserRegisterDto(BaseModel):
    email: EmailStr
    password: constr(regex=r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=\S+$).{8,}$')
    password2: str

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
