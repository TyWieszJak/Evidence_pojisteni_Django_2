from ninja import Router
from .schemas import SchuzkaOut, SchuzkaIn
from .services import SchuzkaService

router = Router(tags=['Schůzky'])

@router.post("/schuzky/", response=SchuzkaOut)
def create_schuzka(request, data: SchuzkaIn):
    return SchuzkaService.create_schuzka(data)

@router.get("/schuzky/", response=list[SchuzkaOut])
def list_schuzky(request):
    return SchuzkaService.list_schuzky()

@router.get("/schuzky/{schuzka_id}", response=SchuzkaOut)
def get_schuzka(request, schuzka_id: int):
    return SchuzkaService.get_schuzka(schuzka_id)

@router.delete("/schuzky/{schuzka_id}")
def delete_schuzka(request, schuzka_id: int):
    return SchuzkaService.delete_schuzka(schuzka_id)
