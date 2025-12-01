from fastapi import APIRouter
router=APIRouter()
@router.get("/")
def init_router():
    return {"detail":"The API is Working!"}