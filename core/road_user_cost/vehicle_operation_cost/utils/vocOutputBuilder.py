from typing import Dict, Any
from .... import standard_keys as c

def build_voc_output(
    vt: str,
    lane: str,
    velocity: float,
    petrol: float,
    diesel: float,
    SP_ET: float,
    SP_IT: float,
    ML: float,
    TL: float,
    EOL: float,
    OL: float,
    G: float,
    FXC_ET: float,
    FXC_IT: float,
    DC_ET: float,
    DC_IT: float,
    PT: float,
    crew: float,
    CHC: float,
    UPD: float
) -> Dict[str, Any]:
 
    def nn(x):
        # Helper to ensure non-negative values
        return max(x, 0)
    
    return {
        "vehicle_type": vt,
        "lane_type": lane,
        "velocity": {
            c.VALUE: nn(velocity),
            c.UNIT: "kmph"
        },
        "VOC_summary": {
            "distance_related": {
                c.FUEL_COST: {
                    c.PETROL: nn(petrol),
                    c.DIESEL: nn(diesel),
                    c.UNIT: "liters per 1000 km",
                    c.iHTC: False
                },
                c.SP: {
                    c.ET: nn(SP_ET)/100,
                    c.IT: nn(SP_IT)/100,
                    c.UNIT: "Rs/km",
                    c.iHTC: True
                },
                c.ML: {
                    c.VALUE: nn(ML)/100,
                    c.UNIT: "Rs/km",
                    c.iHTC: False
                },
                c.TYRE_LIFE: {
                    c.VALUE: nn(TL),
                    c.UNIT: "km/tyre",
                    c.iHTC: False
                },
                c.ENGINE_OIL: {
                    c.VALUE: nn(EOL),
                    c.UNIT: "liters per 1000 km",
                    c.iHTC: False
                },
                c.OTHER_OIL: {
                    c.VALUE: nn(OL),
                    c.UNIT: "liters per 10000 km",
                    c.iHTC: False
                },
                c.GREASE: {
                    c.VALUE: nn(G),
                    c.UNIT: "kg per 10000 km",
                    c.iHTC: False
                },
            },

            "time_related": {
                c.FIXED_COST: {
                    c.ET: nn(FXC_ET),
                    c.IT: nn(FXC_IT),
                    c.UNIT: "Rs/km",
                    c.iHTC: True
                },
                c.DEPRECIATION_COST: {
                    c.ET: nn(DC_ET),
                    c.IT: nn(DC_IT),
                    c.UNIT: "Rs/km",
                    c.iHTC: True
                },
                c.PASSENGER_TIME_COST: {
                    c.VALUE: nn(PT),
                    c.UNIT: "Rs/km",
                    c.iHTC: False
                },
                c.CREW_COST: {
                    c.VALUE: nn(crew),
                    c.UNIT: "Rs/km",
                    c.iHTC: False
                },
                c.CHC: {
                    c.VALUE: nn(CHC),
                    c.UNIT: "Rs/km",
                    c.iHTC: False
                },
            },

            "utilisation": {
                c.VALUE: nn(UPD),
                c.iHTC: False
            },
            "note": "All Values mentioned here are without WPI adjustments!"
        }
    }
