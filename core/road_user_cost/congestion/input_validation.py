from carriage_width_info import carriagewayStandards

def validate(a, Traffic_Input, debug=False):
    errors = []

    # -----------------------------
    # Validate 'a'
    # -----------------------------
    if not isinstance(a, dict):
        errors.append("'a' must be a dictionary.")
    else:
        for key in ['distanceCost', 'timeCost']:
            if key not in a:
                errors.append(f"'a' must contain '{key}' key.")
            elif not isinstance(a[key], dict):
                errors.append(f"'{key}' in 'a' must be a dictionary.")
            else:
                if 'total' not in a[key]:
                    errors.append(f"'{key}' must contain 'total' breakdown.")
                if 'units' not in a[key]:
                    errors.append(f"'{key}' must contain 'units' key.")

    # -----------------------------
    # Extract values from Traffic_Input
    # -----------------------------
    vehicle_data = Traffic_Input.get("vehicle_data", {})
    additional_inputs = Traffic_Input.get("additional_inputs", {})

    lane_type = additional_inputs.get("alternate_road_carriageway", "2L")
    width = additional_inputs.get("carriage_width_in_m", None)
    vc = additional_inputs.get("volume_capacity_ratio", 1)

    # -----------------------------
    # Validate 'vc'
    # -----------------------------
    if not isinstance(vc, (int, float)) or vc < 0:
        errors.append(f"'vc' must be a non-negative number. Provided: {vc}")

    # -----------------------------
    # Validate 'lane_type'
    # -----------------------------
    if not isinstance(lane_type, str):
        errors.append(f"'lane_type' must be a string. Provided: {lane_type}")
    else:
        available_types, _ = carriagewayStandards.CarriagewayStandards.list_types()
        if lane_type not in available_types:
            errors.append(f"'lane_type' must be one of {available_types}. Provided: {lane_type}")

    # -----------------------------
    # Validate 'vehicle_data'
    # -----------------------------
    if not isinstance(vehicle_data, dict):
        errors.append("'vehicle_data' must be a dictionary.")
    else:
        for vt, vinfo in vehicle_data.items():
            count = vinfo.get("vehicles_per_day")
            if not isinstance(count, (int, float)) or count < 0:
                errors.append(f"Vehicle count for '{vt}' must be non-negative number. Provided: {count}")
            
            # Validate power-weight ratio if present
            pwr = vinfo.get("pwr")
            if pwr is not None:
                if not isinstance(pwr, (int, float)) or pwr <= 0:
                    errors.append(f"power-weight ratio for '{vt}' must be > 0. Provided: {pwr}")

    # -----------------------------
    # Validate carriageway width
    # -----------------------------
    if width is None or not isinstance(width, (int, float)) or width <= 0:
        errors.append(f"'carriage_width_in_m' must be positive number. Provided: {width}")

    # -----------------------------
    # Validate 'debug'
    # -----------------------------
    if not isinstance(debug, bool):
        errors.append(f"'debug' must be a boolean. Provided: {debug}")

    # -----------------------------
    # Raise error if any validation fails
    # -----------------------------
    if errors:
        raise ValueError("\n".join(errors))

    return True
