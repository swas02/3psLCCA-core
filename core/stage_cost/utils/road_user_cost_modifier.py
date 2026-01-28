from typing import Optional, Dict, Any

def road_user_cost_modifier(
    road_user_cost: Dict[str, Any],
    additional_rerouting_distance_km: float,
    input_params: Dict[str, Any],
    duration_days: Optional[int] = None,
    spwf: Optional[float] = None,
    debug: bool = False,
) -> Dict[str, Any]:
    """
    Consolidates daily Road User Costs (RUC) and Carbon Costs into total project costs.
    
    Final Key Alignment:
    - 'ruc_cost' for the main total
    - 'debug' (not debug_data) for the breakdown
    """
    # print("***********************************************")
    # print("road_user_cost = ",road_user_cost)
    # print("additional_rerouting_distance_km = ",additional_rerouting_distance_km)
    # print("input_params = ", input_params)
    # print("duration_days, spwf = ", [duration_days, spwf])
    # print("***********************************************")
    

    # 1. Determine number of days
    days = duration_days if duration_days is not None else 1
    
    # 2. Extract components (Keys verified from your dictionary output)
    try:
        voc_per_km = road_user_cost["vehicle_operation_cost"]["total"]["ET"]
        vot_daily = road_user_cost["value_of_time"]["total_Cost"]
        accident_daily = road_user_cost["accident_cost"]["total_accident_cost_INR_per_day"]
        emission_kg_per_km = road_user_cost["total_carbon_emission"]["total_emission_kgCO2e_per_km"]
    except KeyError as exc:
        raise ValueError(f"Missing road user cost data key: {exc}") from exc

    # 3. Daily RUC Calculation
    daily_ruc = (voc_per_km * additional_rerouting_distance_km) + vot_daily + accident_daily

    # 4. Total Project Cost Calculation
    total_ruc = daily_ruc * days
    
    # 5. Carbon Cost (mtCO2e)
    scc = input_params["general"]["social_cost_of_carbon_per_mtco2e"]
    conv_rate = input_params["general"]["currency_conversion"]
    total_emission_cost = (
        emission_kg_per_km * additional_rerouting_distance_km * days * scc * conv_rate / 1000
    )

    # 6. Apply Present Worth Factor (SPWF)
    if spwf is not None:
        total_ruc *= spwf
        total_emission_cost *= spwf

    # 7. Construct Debug Information
    # Using the key "debug" to satisfy the KeyError in use_stage_cost.py
    debug_info = {
        "daily_rates": {
            "voc_at_distance": round(voc_per_km * additional_rerouting_distance_km, 2),
            "vot": round(vot_daily, 2),
            "accidents": round(accident_daily, 2)
        },
        "duration_days": days,
        "spwf_applied": spwf
    } if debug else {}

    # 8. Return
    return {
        "ruc_cost": round(total_ruc, 2),
        "vehicular_emission_cost": round(total_emission_cost, 2),
        "combined_social_cost": round(total_ruc + total_emission_cost, 2),
        "debug": debug_info 
    }