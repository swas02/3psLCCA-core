import json
from Input import Input
from Input_global import Input_global
from core.main import run_full_lcc_analysis, get_IRC_standard_suggestions

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
life_cycle_construction_cost_breakdown = {
    "initial_construction_cost_rs": 12843979.44,
    "material_carbon_emissions_cost_rs": 2065434.91,
    "superstructure_construction_cost_rs": 9356038.92,
    "total_scrap_value_rs": 2164095.02,
}

# 3. Single point of execution
results = run_full_lcc_analysis(
    Input, life_cycle_construction_cost_breakdown, wpi=wpi, debug=True
)

# results = run_full_lcc_analysis(
#     Input_global, life_cycle_construction_cost_breakdown, debug=True
# )


print("--- LCC Analysis Complete ---")
print(json.dumps(results, indent=2))

# print(get_IRC_standard_suggestions())