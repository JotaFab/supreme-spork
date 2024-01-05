from pydantic import BaseModel, Field

class Item(BaseModel):
    """
    Item model.
    """
    item_code: int = Field(gt=1000000, lt=10000000)
    item_name: str = Field(min_length=1, max_length=70)
    tag: list[str] | None = Field(default=None)
    description: str | None = Field(default=None, max_length=300)
    price: float
    quantity: int = Field(gt=0, lt=10000)
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str