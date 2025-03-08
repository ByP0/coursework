from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Optional


class AddGroup(BaseModel):
    