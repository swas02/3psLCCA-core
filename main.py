import json
from Input import Input
from core.main import run_full_lcc_analysis

input_parameters = Input["maintenance_and_stage_parameters"]
input_parameters["general"] = Input["general_parameters"]

# 1. Define WPI (Standard multipliers)
# (Keep the wpi dictionary exactly as you have it)
wpi = {
    "year": 2024,
    "WPI": {
        "fuelCost": {
            "petrol": 1.8067915690866512,
            "diesel": 1.7733050847457628,
            "engine_oil": 1.4496951219512195,
            "other_oil": 1.6951351351351354,
            "grease": 1.6951351351351354,
        },
        "vehicleCost": {
            "propertyDamage": {
                "small_cars": 1.1395759717314486,
                "big_cars": 1.1395759717314486,
                "two_wheelers": 1.1395759717314486,
                "o_buses": 1.1395759717314486,
                "d_buses": 1.1395759717314486,
                "lcv": 1.1395759717314486,
                "hcv": 1.1395759717314486,
                "mcv": 1.1395759717314486,
            },
            "tyreCost": {
                "small_cars": 1.123991935483871,
                "big_cars": 1.123991935483871,
                "two_wheelers": 1.1336538461538461,
                "o_buses": 1.1702564102564101,
                "d_buses": 1.1702564102564101,
                "lcv": 1.1702564102564101,
                "hcv": 1.1702564102564101,
                "mcv": 1.1702564102564101,
            },
            "spareParts": {
                "small_cars": 1.1395759717314486,
                "big_cars": 1.1395759717314486,
                "two_wheelers": 1.1395759717314486,
                "o_buses": 1.1395759717314486,
                "d_buses": 1.1395759717314486,
                "lcv": 1.1395759717314486,
                "hcv": 1.1395759717314486,
                "mcv": 1.1395759717314486,
            },
            "fixedDepreciation": {
                "small_cars": 1.1388400702987698,
                "big_cars": 1.1388400702987698,
                "two_wheelers": 1.1388400702987698,
                "o_buses": 1.1388400702987698,
                "d_buses": 1.1388400702987698,
                "lcv": 1.1388400702987698,
                "hcv": 1.1388400702987698,
                "mcv": 1.1388400702987698,
            },
        },
        "commodityHoldingCost": {
            "small_cars": 1.4788593903638152,
            "big_cars": 1.4788593903638152,
            "two_wheelers": 1.4788593903638152,
            "o_buses": 1.4788593903638152,
            "d_buses": 1.4788593903638152,
            "lcv": 1.4788593903638152,
            "hcv": 1.4788593903638152,
            "mcv": 1.4788593903638152,
        },
        "passengerCrewCost": {
            "Passenger Cost": 1.2706270627062706,
            "Crew Cost": 1.2706270627062706,
        },
        "medicalCost": {
            "fatal": 1.0867924528301887,
            "major": 1.0867924528301887,
            "minor": 1.0867924528301887,
        },
        "votCost": {
            "small_cars": 1.2706270627062706,
            "big_cars": 1.2706270627062706,
            "two_wheelers": 1.2706270627062706,
            "o_buses": 1.2706270627062706,
            "d_buses": 1.2706270627062706,
            "lcv": 1.2706270627062706,
            "hcv": 1.2706270627062706,
            "mcv": 1.2706270627062706,
        },
    },
}


# 2. Define Construction Costs
construction_costs = {
    "initial_cost_of_construction_rs": 12843979.44,
    "cost_of_initial_carbon_emissions_in_rs": 2065434.91,
    "cost_of_super_structure": 9356038.92
}

# 3. Single point of execution
results = run_full_lcc_analysis(Input, wpi, construction_costs, debug=True)

print("--- LCC Analysis Complete ---")
print(json.dumps(results, indent=2))
