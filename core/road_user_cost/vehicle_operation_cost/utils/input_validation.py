from ...carriage_width_info import carriagewayStandards
from . import constants as constants
from .... import standard_keys as c

def validate_input(vehicle_input):
    errors = []

    # -----------------------------
    # 1. Validate lane_type using carriagewayStandards
    # -----------------------------
    available_types, _ = carriagewayStandards.CarriagewayStandards.list_types()
    lane_type = vehicle_input.get("lane_type")

    if not isinstance(lane_type, str):
        errors.append("lane_type must be a string.")
    else:
        if lane_type not in available_types:
            errors.append(
                f"lane_type '{lane_type}' is invalid. Allowed: {available_types}" 
            )

    # -----------------------------
    # 2. Validate Temporal/Peak Hour Logic
    # -----------------------------
    # We ensure the hourly distribution is a valid list of percentages [cite: 191]
    hourly_dist = vehicle_input.get(c.PEAK_HOURLY_DISTRIBUTION)
    h_capacity = vehicle_input.get(c.HOURLY_CAPACITY)

    if hourly_dist is not None:
        if not isinstance(hourly_dist, list):
            errors.append(f"{c.PEAK_HOURLY_DISTRIBUTION} must be a list of percentages.")
        else:
            if not all(isinstance(x, (int, float)) for x in hourly_dist):
                errors.append("All elements in peak hourly distribution must be numeric.")
            
            # Sum of percentages must not exceed 100% (1.0)
            total_share = sum(hourly_dist)
            if total_share > 1.0:
                errors.append(f"Sum of peak traffic percentages ({total_share}) cannot exceed 1.0.")
            
            # Cannot have more than 24 hours in a day
            if len(hourly_dist) > 24:
                errors.append("Peak hourly distribution cannot exceed 24 hours.")

    if h_capacity is not None:
        if not isinstance(h_capacity, (int, float)) or h_capacity <= 0:
            errors.append(f"{c.HOURLY_CAPACITY} must be a positive number.")

    # -----------------------------
    # 3. Validate carriageway width logic
    # -----------------------------
    if lane_type == c.EW: 
        custom_width = vehicle_input.get("carriageway_width") 
        if custom_width is None or not isinstance(custom_width, (int, float)) or custom_width <= 0: 
            errors.append(
                "For Expressway type, 'carriageway_width' must be a positive number (custom width required)."
            )
    else:
        standard_width, msg = carriagewayStandards.CarriagewayStandards.get_width(lane_type)
        if standard_width is None:
            errors.append(f"Could not retrieve standard width: {msg}")
        else:
            vehicle_input["carriageway_width"] = standard_width

    # -----------------------------
    # 4. Validate numeric fields
    # -----------------------------
    numeric_fields = ["rg_roughness_factor", "fl_fall_factor", "rs_rise_factor"]

    for field in numeric_fields:
        value = vehicle_input.get(field)
        if not isinstance(value, (int, float)):
            errors.append(f"{field} must be a number (int or float).")

    # -----------------------------
    # 5. Validate vehicle_info
    # -----------------------------
    vehicle_info = vehicle_input.get("vehicle_info")
    if not isinstance(vehicle_info, dict):
        errors.append("vehicle_info must be a dictionary.")
    else:
        # Check for missing or invalid vehicle types [cite: 298, 299]
        missing_keys = [vtype for vtype in constants.vehicle_type_list if vtype not in vehicle_info]
        if missing_keys:
            errors.append(f"Missing vehicle types in vehicle_info: {missing_keys}. All must be present.")

        invalid_keys = [vtype for vtype in vehicle_info if vtype not in constants.vehicle_type_list]
        if invalid_keys:
            errors.append(f"Invalid vehicle types in vehicle_info: {invalid_keys}. Allowed: {constants.vehicle_type_list}")

        for vtype, count in vehicle_info.items():
            if not isinstance(count, (int, float)) or count < 0:
                errors.append(f"Count for '{vtype}' must be a non-negative number.")

    # -----------------------------
    # 6. Validate power_weight_ratio_pwr for HCV, MCV
    # -----------------------------
    mcv_count = vehicle_info.get(c.MCV, 0)
    hcv_count = vehicle_info.get(c.HCV, 0)

    if mcv_count > 0 or hcv_count > 0:
        pwr = vehicle_input.get("power_weight_ratio_pwr")
        if pwr is None:
            errors.append("power_weight_ratio_pwr must be provided if LCV, HCV, or MCV count > 0.")
        elif isinstance(pwr, dict):
            for vt in [c.MCV, c.HCV]:
                if vehicle_info.get(vt, 0) > 0:
                    if vt not in pwr or not isinstance(pwr[vt], (int, float)) or pwr[vt] <= 0:
                        errors.append(f"power_weight_ratio_pwr for '{vt}' is required and must be > 0.")
        elif not isinstance(pwr, (int, float)) or pwr <= 0:
            errors.append("power_weight_ratio_pwr must be numeric and > 0.")

    if errors:
        raise ValueError("\n".join(errors))

    return True