from .vehicle_operation_cost import core as VOC
from .congestion import core as congestion
from .value_of_time import main as value_of_time
from .accident_cost import core as accident_cost
from .total_carbon_emission import core as total_carbon_emission
from .calculate_total_ruc_per_day import calculate_total_ruc_per_day


def calculate_road_user_costs(traffic_input, wpi, debug=False):
    """
    Coordinator for Road User Cost (RUC).
    Optimized to return only the final, congestion-adjusted VOC.
    """
    # Get additional reroute distance in km
    additional_rerouting_distance_km = traffic_input["additional_inputs"]["additional_reroute_distance_km"]

    # 1. Accident Cost
    ac = accident_cost.accident_cost(traffic_input, wpi, debug)

    # 2. Base VOC Calculation (Internal)
    # We need voc_raw to get the Rs/km per vehicle type based on road geometry
    voc_raw, _ = VOC.main(traffic_input, wpi, debug)

    # 3. Final VOC (Congestion Adjusted)
    # This is your true Vehicle Operating Cost including temporal traffic impacts
    voc_final = congestion.calculate_total_adjusted_costs(
        voc_raw, traffic_input, debug)

    # 4. Value of Time (VOT)
    vot = value_of_time.calculate_additional_time_cost(
        traffic_input, wpi, debug)

    # 5. Total Carbon Emission
    tce = total_carbon_emission.calculate_total_carbon_emission(
        traffic_input["vehicle_data"], additional_rerouting_distance_km, debug)

    result = {
        "accident_cost": ac,
        "vehicle_operation_cost": voc_final,
        "value_of_time": vot,
        "total_carbon_emission": tce
    }
    return calculate_total_ruc_per_day(result, additional_rerouting_distance_km)