from pydantic import BaseModel


class Vector3DCreate(BaseModel):
    id: int
    x: float
    y: float
    z: float


class Vector3DRead(BaseModel):
    id: int
    x: float
    y: float
    z: float

    model_config = {"from_attributes": True}
