from enum import Enum

class HousingType(Enum):
    RENT = "rent"
    BUY = "buy"


class RealEstateType(Enum):
    HOUSE = "house"
    FLAT = "flat"

class Table(Enum):
    DIM_FEATURE = "feature"
    DIM_LOCATION = "location"
    DIM_SELLER = "seller"
    FACT_REAL_ESTATE = "real estate"
    REAL_ESTATE_FINAL = "real estate final"