from ...services.manager import manager
from ...models.contract import ContractUpdate
from fastapi import APIRouter

# Create a new router for update endpoints
router = APIRouter()

@router.post("/update")
async def update_contract(update: ContractUpdate):
    """REST endpoint to broadcast a contract update to all clients."""
    successful = await manager.broadcast(update.model_dump())
    return {
        "broadcasted_to": successful,
        **update.model_dump()
    }