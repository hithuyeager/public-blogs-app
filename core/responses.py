from pydantic import BaseModel
from typing import Dict,Optional,Any

class APIResponse(BaseModel):
   status: str
   data: Optional[Any]