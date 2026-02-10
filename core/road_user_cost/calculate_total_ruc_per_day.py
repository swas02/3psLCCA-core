from typing import Dict, Any


def calculate_total_ruc_per_day(
    road_user_cost: Dict[str, Any],
    additional_rerouting_distance_km: float,
    debug: bool = False,
) -> Dict[str, Any]:
    """
    Calculates total Road User Cost (RUC) per day.
    """

    try:
        voc_per_km = road_user_cost["vehicle_operation_cost"]["total"]["ET"]
        vot_daily = road_user_cost["value_of_time"]["total_Cost"]
        accident_daily = road_user_cost["accident_cost"]["total_accident_cost_INR_per_day"]
    except KeyError as exc:
        raise ValueError(f"Missing road user cost data key: {exc}") from exc

    # Per-day RUC
    daily_ruc = (
        voc_per_km * additional_rerouting_distance_km
        + vot_daily
        + accident_daily
    )

    # debug_info = {
    #     "components": {
    #         "vehicle_operation_cost": round(voc_per_km * additional_rerouting_distance_km, 2),
    #         "value_of_time": round(vot_daily, 2),
    #         "accident_cost": round(accident_daily, 2),
    #     }
    # } if debug else {}
    road_user_cost["total_daily_ruc"] = round(daily_ruc, 3)
    return road_user_cost
