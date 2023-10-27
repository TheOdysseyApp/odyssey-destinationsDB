# complex types define in here to perform type checking
from pydantic import BaseModel


# mapping from python class type to dynamodb data type
# TODO: finish this map for easier item data creation
DATA_MAP = {
    str: "S",
    float: "N",
    dict: "M",
}


class CostOfLiving(BaseModel):
    amount: float
    currency: str


class Transportation(BaseModel):
    pass


class Safety(BaseModel):
    pass