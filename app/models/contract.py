from pydantic import BaseModel
from app.resource.location import Location
from app.resource.status import Status



class ContractUpdate(BaseModel):
    """Pydantic model for contract update payloads."""
    location: Location
    status: Status
 