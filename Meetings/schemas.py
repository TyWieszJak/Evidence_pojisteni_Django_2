from ninja import Schema
from datetime import datetime

# Výstupní schéma (odpověď API)
class SchuzkaOut(Schema):
    id: int
    datum_cas: datetime
    poznamka: str | None
    pojistenec_id: int

# Vstupní schéma (vstupní data pro API)
class SchuzkaIn(Schema):
    datum_cas: datetime
    poznamka: str | None
    pojistenec_id: int
