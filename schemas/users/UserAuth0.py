from pydantic import EmailStr, constr

from schemas.base import BaseSchema


class UserAuth0(BaseSchema):

    first_name: constr(max_length=50, min_length=1)
    last_name: constr(max_length=50, min_length=1)
    email: EmailStr
