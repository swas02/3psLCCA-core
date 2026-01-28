from .road_user_cost.main import calculate_road_user_costs
from .stage_cost.stage_cost import StageCostCalculator
from .utils.dump_to_file import dump_to_file


def run_full_lcc_analysis(input_data, wpi, construction_costs, debug=False):
    """
    Entry point for the OSDAG LCC module. 
    Coordinates RUC calculations and Life Cycle Stage Costing.
    """

    # 1. Execute Road User Cost Calculations
    ruc_results = calculate_road_user_costs(
        input_data["traffic_and_road_data"], wpi, debug)

    # 2. Setup Stage Cost Parameters
    stage_params = input_data["maintenance_and_stage_parameters"].copy()
    stage_params["general"] = input_data["general_parameters"]

    # Inject the distance into general params so the calculator/modifier can find it
    stage_params["general"]["additional_rerouting_distance_km"] = input_data["traffic_and_road_data"].get(
        "additional_inputs").get("additional_reroute_distance_km")

    # 4. Combine initial asset costs with formatted RUC results
    construction_costs["road_user_cost"] = ruc_results

    if debug:
        dump_to_file("Stage_Cost_Calculator_Inputs.json", {"stage_params": stage_params,
                                                           "construction_costs": construction_costs})

    # 5. Initialize and Run LCC Analysis
    stage_calc = StageCostCalculator(stage_params, construction_costs, debug)


    return {
        "initial_stage": stage_calc.initial_cost_calculator(),
        "use_stage": stage_calc.use_stage_cost_calculator(),
        "reconstruction": stage_calc.reconstruction(),
        "end_of_life": stage_calc.end_of_life_stage_costs()
    }
