def validate_vehicle_data(vehicle_data: dict) -> tuple[bool, list[str]]:
    """
    Validate the structure and values of the vehicle data dictionary.

    Parameters:
    ----------
    vehicle_data : dict
        The vehicle data to validate.

    Returns:
    -------
    tuple
        - is_valid (bool): True if the data is valid, False otherwise.
        - errors (list): List of error messages if validation fails.
    """
    errors = []

    if not isinstance(vehicle_data, dict):
        errors.append("vehicle_data must be a dictionary.")
        return False, errors

    if not vehicle_data:
        errors.append("vehicle_data cannot be an empty dictionary.")
        return False, errors

    # Validate each vehicle's data
    for vehicle_type, data in vehicle_data.items():
        if not isinstance(data, dict):
            errors.append(f"Invalid format for vehicle '{vehicle_type}': data must be a dictionary.")
            continue

        # Check for 'vehicles_per_day'
        if 'vehicles_per_day' not in data or not isinstance(data['vehicles_per_day'], (int, float)):
            errors.append(f"'{vehicle_type}' is missing 'vehicles_per_day' or it's not a valid number.")
        elif data['vehicles_per_day'] <= 0:
            errors.append(f"'{vehicle_type}' must have a positive 'vehicles_per_day' value.")

        # Check for 'carbon_emissions_kgCO2e_per_km'
        if 'carbon_emissions_kgCO2e_per_km' not in data or not isinstance(data['carbon_emissions_kgCO2e_per_km'], (int, float)):
            errors.append(f"'{vehicle_type}' is missing 'carbon_emissions_kgCO2e_per_km' or it's not a valid number.")
        elif data['carbon_emissions_kgCO2e_per_km'] <= 0:
            errors.append(f"'{vehicle_type}' must have a positive 'carbon_emissions_kgCO2e_per_km' value.")

    # Return validation result
    is_valid = len(errors) == 0
    return is_valid, errors
