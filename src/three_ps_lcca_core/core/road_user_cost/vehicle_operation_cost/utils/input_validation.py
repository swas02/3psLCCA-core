from ...carriage_width_info import carriagewayStandards
from . import constants as constants
from .... import standard_keys as c

def validate_input(vehicle_input):
    errors = []
    info = []

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
    # 2. Validate carriageway width logic
    # -----------------------------

    standard_width, msg = carriagewayStandards.CarriagewayStandards.get_width(
        lane_type)

    custom_width = vehicle_input.get("carriageway_width")

    if standard_width is None:
        # No standard exists, user must provide a valid width
        if not isinstance(custom_width, (int, float)) or custom_width <= 0:
            errors.append(
                f"No standard width for '{lane_type}'. Provide a positive 'carriageway_width'.")

    else:
        # Standard exists
        if custom_width is None:
            vehicle_input["carriageway_width"] = standard_width
        elif custom_width != standard_width:
            info.append(
                f"User-provided width ({custom_width} m) differs from standard ({standard_width} m).")

    # -----------------------------
    # 3. Validate numeric fields
    # -----------------------------
    numeric_fields = ["rg_roughness_factor",
                      "fl_fall_factor", "rs_rise_factor"]

    for field in numeric_fields:
        value = vehicle_input.get(field)
        if not isinstance(value, (int, float)):
            errors.append(f"{field} must be a number (int or float).")

    # -----------------------------
    # 4. Validate vehicle_info
    # -----------------------------
    vehicle_info = vehicle_input.get("vehicle_info")
    if not isinstance(vehicle_info, dict):
        errors.append("vehicle_info must be a dictionary.")
    else:
        # Check for missing or invalid vehicle types [cite: 298, 299]
        missing_keys = [
            vtype for vtype in constants.vehicle_type_list if vtype not in vehicle_info]
        if missing_keys:
            errors.append(
                f"Missing vehicle types in vehicle_info: {missing_keys}. All must be present.")

        invalid_keys = [
            vtype for vtype in vehicle_info if vtype not in constants.vehicle_type_list]
        if invalid_keys:
            errors.append(
                f"Invalid vehicle types in vehicle_info: {invalid_keys}. Allowed: {constants.vehicle_type_list}")

        for vtype, count in vehicle_info.items():
            if not isinstance(count, (int, float)) or count < 0:
                errors.append(
                    f"Count for '{vtype}' must be a non-negative number.")

    # -----------------------------
    # 5. Validate power_weight_ratio_pwr for HCV, MCV
    # -----------------------------
    mcv_count = vehicle_info.get(c.MCV, 0)
    hcv_count = vehicle_info.get(c.HCV, 0)

    if mcv_count > 0 or hcv_count > 0:
        pwr = vehicle_input.get("power_weight_ratio_pwr")
        if pwr is None:
            errors.append(
                "power_weight_ratio_pwr must be provided if LCV, HCV, or MCV count > 0.")
        elif isinstance(pwr, dict):
            for vt in [c.MCV, c.HCV]:
                if vehicle_info.get(vt, 0) > 0:
                    if vt not in pwr or not isinstance(pwr[vt], (int, float)) or pwr[vt] <= 0:
                        errors.append(
                            f"power_weight_ratio_pwr for '{vt}' is required and must be > 0.")
        elif not isinstance(pwr, (int, float)) or pwr <= 0:
            errors.append("power_weight_ratio_pwr must be numeric and > 0.")

    if errors:
        raise ValueError("\n".join(errors))

    return True, info
