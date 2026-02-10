from .road_user_cost.main import calculate_road_user_costs
from .stage_cost.stage_cost import StageCostCalculator
from .utils.dump_to_file import dump_to_file
from .utils.list_suggestions import get_IRC_standard_suggestions
from .utils.input_validator import ironclad_validator


def run_full_lcc_analysis(input_data, construction_costs, wpi=None, debug=False):
    """
    Entry point for the OSDAG LCC module.
    Validates input, coordinates Road User Cost (RUC) calculations, and
    computes Life Cycle Stage Costs.

    Args:
        input_data (dict): Project input dictionary.
        construction_costs (dict): Initial construction costs.
        wpi (float, optional): Wholesale price index for RUC calculation.
        debug (bool, optional): If True, dumps intermediate inputs to JSON.

    Returns:
        dict: Stage-wise LCC results (initial, use, reconstruction, end-of-life).

    Raises:
        ValueError: If input fails validation or wpi is required but not provided.
    """

    # --- 1. Load standard suggestions for validation ---
    suggestions = get_IRC_standard_suggestions()

    # --- 2. Validate Input ---
    validation_report = ironclad_validator(input_data, suggestions, wpi)

    if validation_report["errors"]:
        # Stop execution if there are critical errors
        raise ValueError(
            f"Input validation failed with errors:\n{validation_report['errors']}"
        )

    if debug and validation_report["warnings"]:
        print("Validation warnings:", validation_report["warnings"])

    # --- 3. Determine if RUC calculation is bypassed ---
    bypass_ruc = input_data.get("general_parameters", {}).get(
        "use_global_road_user_calculations", False
    )

    if bypass_ruc:
        # Use provided RUC from input_data
        ruc_results = input_data.get(
            "daily_road_user_cost_with_vehicular_emissions", {}
        )
        if debug:
            print("Bypassing RUC calculation. Using provided RUC:", ruc_results)

    else:
        if wpi is None:
            raise ValueError("wpi cannot be None when RUC calculation is required")

        # Calculate RUC normally
        traffic_data = input_data.get("traffic_and_road_data", {})
        ruc_results = calculate_road_user_costs(traffic_data, wpi, debug)

    # --- 4. Prepare Stage Cost Parameters ---
    stage_params = input_data.get("maintenance_and_stage_parameters", {}).copy()
    stage_params["general"] = input_data.get("general_parameters", {})

    # Add RUC results to construction costs
    construction_costs["daily_road_user_cost_with_vehicular_emissions"] = ruc_results

    if debug:
        dump_to_file(
            "Stage_Cost_Calculator_Inputs.json",
            {"stage_params": stage_params, "construction_costs": construction_costs},
        )

    # --- 5. Initialize and Run LCC Calculations ---
    stage_calc = StageCostCalculator(stage_params, construction_costs, debug)

    return {
        "initial_stage": stage_calc.initial_cost_calculator(),
        "use_stage": stage_calc.use_stage_cost_calculator(),
        "reconstruction": stage_calc.reconstruction(),
        "end_of_life": stage_calc.end_of_life_stage_costs(),
    }
