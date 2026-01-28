import os
import json
from datetime import datetime
from .input_validation import validate_vehicle_data

def calculate_total_carbon_emission(vehicle_data: dict, debug: bool = False) -> dict[str, float | str]:
    """
    Calculate total carbon emissions (kgCO2e per km) for all vehicles.

    Total = sum(vehicles_per_day * carbon_emissions_kgCO2e_per_km)

    Parameters
    ----------
    vehicle_data : dict
        traffic_input["vehicle_data"]
    debug : bool
        If True, saves a detailed emission breakdown JSON in ./debug/

    Returns
    -------
    float
        Total carbon emissions in kgCO2e per km (per day of traffic)

    Raises
    ------
    ValueError
        If vehicle_data is missing or not a dictionary
    """

    # Validate the vehicle_data
    is_valid, validation_errors = validate_vehicle_data(vehicle_data)
    if not is_valid:
        raise ValueError(f"Invalid vehicle_data: {validation_errors}")

    total_emission = 0.0
    breakdown = {}

    # Process each vehicle type
    for vehicle_type, data in vehicle_data.items():
        count = data.get("vehicles_per_day")
        emission_factor = data.get("carbon_emissions_kgCO2e_per_km")

        try:
            vehicle_total = float(count) * float(emission_factor)
        except (ValueError, TypeError):
            print(f"Warning: Skipping {vehicle_type}, invalid numeric values.")
            continue

        total_emission += vehicle_total

        breakdown[vehicle_type] = {
            "vehicles_per_day": count,
            "emission_factor_kgCO2e_per_km": emission_factor,
            "total_emission_kgCO2e_per_km": vehicle_total
        }

    if debug:
        os.makedirs("debug", exist_ok=True)

        debug_output = {
            "timestamp": datetime.now().isoformat(),
            "unit": "kgCO2e_per_km (per day of traffic)",
            "total_emission_kgCO2e_per_km": total_emission,
            "vehicle_breakdown": breakdown
        }

        debug_file = os.path.join("debug", "traffic_carbon_emission_breakdown.json")
        with open(debug_file, "w", encoding="utf-8") as f:
            json.dump(debug_output, f, indent=4)

    return {
        "total_emission_kgCO2e_per_km": total_emission,
        "unit": "kgCO2e/km/day",
        "Note": "This value represents the total carbon emissions per kilometer per day. "
        "To get the total emissions for a specific period or distance, multiply this value "
        "by the number of days and the total distance traveled (in km)."
    }
