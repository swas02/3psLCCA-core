from typing import Dict, Any, TypedDict
import vehicle_operation_cost.utils.IRCSP302019TableC1
from vehicle_operation_cost.utils.vocOutputBuilder import build_voc_output
from vehicle_operation_cost.utils.commonInputs import VehicleInput, extract_vehicle_inputs

Vehicle = ""


def compute_voc(vehicle_input: VehicleInput) -> Dict[str, Any]:
    vt, W, RG, FL, RS, lane, RF = extract_vehicle_inputs(vehicle_input)
    NP: Dict[str, int] = vehicle_operation_cost.utils.IRCSP302019TableC1.vehicle_costs[Vehicle]

    if vt == Vehicle:
        # -----------------------------
        # SPEED FORMULA
        # -----------------------------
        speed_map: Dict[str, float] = {
        }

        V: float = speed_map.get(lane, 0.0)

        # -----------------------------
        # DISTANCE RELATED
        # -----------------------------

        # Fuel consumption
        petrol: float = 0
        diesel: float = 0
        fuel: float = 0 

        # Spare parts
        SP_ET: float = 0 * NP["without_taxes"]
        SP_IT: float = 0 * NP["with_taxes"]

        # Maintenance labour
        ML: float = 0

        # Tyre life
        TL: float = 0

        # Engine oil
        EOL: float = 0

        # Other oil
        OL: float = 0

        # Grease
        G: float = 0

        total_dist_related_cost: float = fuel + SP_ET + ML + TL + EOL + OL + G

        # -----------------------------
        # TIME RELATED
        # -----------------------------

        # Utilisation
        UPD: float = 0

        # Fixed costs
        FXC_ET: float = 0
        FXC_IT: float = 0

        # Depreciation costs
        DC_ET: float = 0
        DC_IT: float = 0

        # Passenger time cost
        if lane in ["SL", "IL"]:
            PT: float = 0
        elif lane == "2L":
            PT = 0
        else:
            PT = 0

        # Crew cost
        crew: float = 0.0

        # Commodity holding cost
        CHC: float = 0.0

        total_time_related_cost: float = FXC_ET + DC_ET + PT + crew + CHC

        # -----------------------------
        # BUILD FINAL OUTPUT
        # -----------------------------
        return build_voc_output(
            vt=vt, lane=lane,
            velocity=V,
            petrol=petrol, diesel=diesel,
            SP_ET=SP_ET, SP_IT=SP_IT,
            ML=ML, TL=TL,
            EOL=EOL, OL=OL, G=G,
            FXC_ET=FXC_ET, FXC_IT=FXC_IT,
            DC_ET=DC_ET, DC_IT=DC_IT,
            PT=PT, crew=crew, CHC=CHC,
            UPD=UPD
        )

    else:
        raise NotImplementedError(
            f"VOC computation for vehicle type '{vt}' is not implemented yet."
        )
