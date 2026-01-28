import os
import json
from .IRCSP302019Table8_Table9 import (
    table8_Economic_Cost_for_Different_Type_of_Accidents,
    table9_Economic_Cost_of_Quantum_of_Vehicle_Damage_due_to_Accidents
)
from .input_validation import validate_accident_input
from ... import standard_keys as c
from ...utils.dump_to_file import dump_to_file


def accident_cost(traffic_input, wpi, debug=False):
    """
    Calculates total accident cost. 
    Corrects for daily vs annual scaling and maps d_buses to o_buses.
    """
    is_valid, errors = validate_accident_input(traffic_input, wpi)
    if not is_valid:
        # Stop execution and tell the user exactly what is missing
        raise ValueError(
            f"Accident Input Validation Failed: {', '.join(errors)}")

    # 1. Extract Inputs (Explicit assignments)
    add_in = traffic_input['additional_inputs']
    vehicle_data = traffic_input['vehicle_data']
    severity_dist_percent = traffic_input['accident_severity_distribution']

    # 2. Exposure-Based Total Accident Calculation
    total_adt = sum(v["vehicles_per_day"] for v in vehicle_data.values())
    dist_km = add_in["additional_reroute_distance_km"]
    crash_rate_annual = add_in["crash_rate_accidents_per_million_km"]
    wz_multiplier = add_in["work_zone_multiplier"]

    # --- FIXED: Annual to Daily Scaling ---
    # If the crash rate is annual per million km
    total_daily_accidents = (
        crash_rate_annual * wz_multiplier * dist_km) / 1000000
    # 3. Human Cost & Count Distribution
    human_cost_table = table8_Economic_Cost_for_Different_Type_of_Accidents()
    human_cost = 0
    calculated_severity_counts = {}
    human_breakdown = {}

    for severity, weight in severity_dist_percent.items():
        severity_count = total_daily_accidents * weight / 100
        calculated_severity_counts[severity] = round(severity_count, 8)

        base_cost = human_cost_table[severity]
        wpi_factor = wpi["WPI"]["medicalCost"][severity]
        adjusted_cost = base_cost * wpi_factor

        total_sev_cost = severity_count * adjusted_cost
        human_cost += total_sev_cost

        if debug:
            human_breakdown[severity] = {
                "count": round(severity_count, 8),
                "total_cost": round(total_sev_cost, 2)
            }

    # 4. Vehicle Damage Cost (Mapping d_buses -> o_buses)
    damage_table = table9_Economic_Cost_of_Quantum_of_Vehicle_Damage_due_to_Accidents()
    vehicle_damage_cost = 0
    damage_breakdown = {}

    for v_key, v_info in vehicle_data.items():
        # --- FIXED: If vehicle is d_buses, use o_buses data ---
        lookup_key = c.O_BUSES if v_key == c.D_BUSES else v_key

        veh_adt = v_info["vehicles_per_day"]
        # Share of total accidents based on vehicle share of traffic volume
        veh_accident_share = (veh_adt / total_adt) * total_daily_accidents

        base_dmg_cost = damage_table[lookup_key]
        wpi_factor = wpi["WPI"]["vehicleCost"]["propertyDamage"][lookup_key]
        adj_dmg_cost = base_dmg_cost * wpi_factor

        total_veh_dmg_cost = veh_accident_share * adj_dmg_cost
        vehicle_damage_cost += total_veh_dmg_cost

        if debug:
            damage_breakdown[v_key] = {
                "lookup_key_used": lookup_key,
                "accident_share": round(veh_accident_share, 8),
                "cost": round(total_veh_dmg_cost, 2)
            }

    # 5. Final Result
    total_cost = human_cost + vehicle_damage_cost

    result = {
        "total_accident_cost_INR_per_day": round(total_cost, 2),
        "human_cost_INR_per_day": round(human_cost, 2),
        "vehicle_damage_cost_INR_per_day": round(vehicle_damage_cost, 2),
        "calculated_total_daily_accidents": round(total_daily_accidents, 8),
        "accident_severity_distribution_counts": calculated_severity_counts
    }

    if debug:
        dump_to_file("accident_cost_summary.json", {
            "summary": result,
            "human_breakdown": human_breakdown,
            "damage_breakdown": damage_breakdown
        })

    return result
