from pydantic import BaseModel, ConfigDict

class BaseValidation(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True
    )

