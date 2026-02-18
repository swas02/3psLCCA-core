from typing import TypedDict, Tuple
from ...carriage_width_info.carriagewayStandards import CarriagewayStandards

class VehicleInput(TypedDict):
    vehicle_type: str
    carriageway_width: float
    rg_roughness_factor: float
    fl_fall_factor: float
    rs_rise_factor: float
    lane_type: str
    rf_rise_and_fall_factor: float
    power_weight_ratio_pwr: float | None


def extract_vehicle_inputs(vehicle_input: VehicleInput) -> Tuple[
    str, float, float, float, float, str, str, float
]:
    """
    Extracts common vehicle input fields.

    Returns:
        vt   - vehicle type
        W    - carriageway width
        RG   - roughness factor
        FL   - fall factor
        RS   - rise factor
        lane - mapped to correspond with the lane classifications defined in IRC SP 30.
        RF   - rise and fall factor
    """
    vt: str = vehicle_input["vehicle_type"]
    W: float = vehicle_input["carriageway_width"]
    RG: float = vehicle_input["rg_roughness_factor"]
    FL: float = vehicle_input["fl_fall_factor"]
    RS: float = vehicle_input["rs_rise_factor"]
    input_lane: str = vehicle_input["lane_type"]
    lane: str = CarriagewayStandards.get_velocity_class(input_lane)
    RF: float = vehicle_input["rf_rise_and_fall_factor"]

    return vt, W, RG, FL, RS, input_lane, lane, RF
