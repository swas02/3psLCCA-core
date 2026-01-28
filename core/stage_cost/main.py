# import json
# from stage_cost import StageCostCalculator
# from typing import Dict, Any, Optional
# from utils.road_user_cost_modifier import road_user_cost_modifier


# input_parameters = {
#     "general": {
#         "service_life_years": 50,
#         "analysis_period_years": 150,
#         "discount_rate_percent": 6.7,
#         "inflation_rate_percent": 5.15,
#         "interest_rate_percent": 7.75,
#         "investment_ratio": 0.5,
#         "social_cost_of_carbon_per_mtco2e": 86.40,
#         "construction_period_months": 5.2,
#         "working_days_per_month": 26,
#         "days_per_month": 30,
#         "daily_traffic_volume_pcu_per_day": 20520.45,
#         "vehicle_emission_factor_kgco2_per_km_per_pcu": 0.1213,
#         "demolition_and_disposal_duration_months": 1,
#         "additional_rerouting_distance_km": 0.175,
#         "currency_conversion": 88.73
#     },

#     "use_stage_cost": {
#         "routine": {
#             "inspection": {
#                 "percentage_of_initial_construction_cost_per_year": 0.1,
#                 "interval_in_years": 1
#             },
#             "maintenance": {
#                 "percentage_of_initial_construction_cost_per_year": 0.55,
#                 "percentage_of_initial_cabron_emission_cost": 0.55,
#                 "interval_in_years": 5
#             }
#         },
#         "major": {
#             "inspection": {
#                 "percentage_of_initial_construction_cost": 0.5,
#                 "interval_for_repair_and_rehabitation_in_years": 5,
#             },
#             "repair": {
#                 "percentage_of_initial_construction_cost": 10,
#                 "interval_for_repair_and_rehabitation_in_years": 20,
#                 "percentage_of_initial_carbon_emission_cost": 0.55,
#                 "repairs_duration_months": 3,

#             }
#         },
#         "replacement_costs_for_bearing_and_expansion_joint": {
#             "percentage_of_super_structure_cost": 12.5,
#             "interval_of_replacement_in_years": 25,
#             "duration_of_replacement_in_days": 2
#         }
#     },
#     "end_of_life_stage_costs": {
#         "demolition_and_disposal": {
#             "percentage_of_initial_construction_cost": 10,
#             "percentage_of_initial_carbon_emission_cost": 10,
#             "duration_for_demolition_and_disposal_in_months": 1
#         }
#     }
# }

# input_from_program = {
#     "initial_cost_of_construction_rs": 12843979.44,
#     "cost_of_initial_carbon_emissions_in_rs": 2065434.91,
#     "cost_of_super_structure": 9356038.92,
#     "road_user_cost": {
#         "accident_cost": {
#             "total_accident_cost_INR": 1625.989054586024,
#             "human_cost_INR": 1107.4604084911698,
#             "vehicle_damage_cost_INR": 518.5286460948543,
#             "note": "This result is unit-independent. The input accidents are assumed to be the total number of accidents over the analysis period. If you provide accidents per day, you should multiply by the number of days of analysis.",
#         },
#         "vehicle operation cost (without congestion)": {
#             "distance_total": {"IT": 254012.70933299456, "ET": 116680.93201248567},
#             "time_total": {"IT": 156994.04289106757, "ET": 150249.2262201217},
#             "total": {"IT": 411006.7522240621, "ET": 266930.15823260735},
#             "unit": "Rs/km",
#         },
#         "vehicle operation cost (with congestion)": {
#             "distance_total": {"IT": 382896.63572800753, "ET": 177278.33017419677},
#             "time_total": {"IT": 244718.6340772727, "ET": 234408.85248841607},
#             "total": {"IT": 627615.2698052803, "ET": 411687.1826626129},
#             "unit": "Rs/km",
#         },
#         "value_of_time": {"total_Cost": 72610.8531562775, "unit": "Rs./day"},
#         "total_carbon_emission": {
#             "total_emission_kgCO2e_per_km": 4412.82967,
#             "unit": "kgCO2e/km/day",
#             "Note": "This value represents the total carbon emissions per kilometer per day. To get the total emissions for a specific period or distance, multiply this value by the number of days and the total distance traveled (in km).",
#         },
#     }

# }

# # -------------------------------------------------
# # RUN
# # -------------------------------------------------
# stage_cost = StageCostCalculator(
#     input_parameters,
#     input_from_program,
#     debug=False
# )

# use_stage_cost = stage_cost.use_stage_cost_calculator()
# print(json.dumps(use_stage_cost, indent=4))

# reconstruction = stage_cost.reconstruction()
# print(json.dumps(reconstruction, indent=4))


# end_of_life_stage = stage_cost.end_of_life_stage_costs()
# print(json.dumps(end_of_life_stage, indent=4))
