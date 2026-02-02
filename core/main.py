from .road_user_cost.main import calculate_road_user_costs
from .stage_cost.stage_cost import StageCostCalculator
from .utils.dump_to_file import dump_to_file


def run_full_lcc_analysis(input_data, wpi, construction_costs, debug=False):
    """
    Entry point for the OSDAG LCC module. 
    Coordinates RUC calculations and Life Cycle Stage Costing.
    
    If 'bypass_road_user_calculations' is True in general_parameters,
    the function will use 'road_user_cost' from input_data instead of
    calculating it.
    """

    # Execute Road User Cost Calculations or Bypass
    bypass_ruc = input_data.get("general_parameters", {}).get("bypass_road_user_calculations", False)

    if bypass_ruc:
        # Use provided RUC from input_data
        ruc_results = input_data["daily_road_user_cost_with_vehicular_emissions"]
        if debug:
            print("Bypassing RUC calculation. Using provided road_user_cost:", ruc_results)
    else:
        # Calculate RUC normally
        ruc_results = calculate_road_user_costs(input_data.get("traffic_and_road_data", {}), wpi, debug)
        # print(ruc_results)

    # Setup Stage Cost Parameters
    stage_params = input_data.get("maintenance_and_stage_parameters", {}).copy()
    stage_params["general"] = input_data.get("general_parameters", {})


    # Combine initial asset costs with RUC results
    construction_costs["daily_road_user_cost_with_vehicular_emissions"] = ruc_results

    if debug:
        dump_to_file(
            "Stage_Cost_Calculator_Inputs.json",
            {"stage_params": stage_params, "construction_costs": construction_costs}
        )

    # Initialize and Run LCC Analysis
    stage_calc = StageCostCalculator(stage_params, construction_costs, debug)

    return {
        "initial_stage": stage_calc.initial_cost_calculator(),
        "use_stage": stage_calc.use_stage_cost_calculator(),
        "reconstruction": stage_calc.reconstruction(),
        "end_of_life": stage_calc.end_of_life_stage_costs()
    }
