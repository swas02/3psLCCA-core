Input = {
    "project_metadata": {
        "description": "Common input for OSDAG LCC Analysis",
        "standard": "IRC 106:1990 / IRC SP 30-2019"
    },
    "general_parameters": {
        "service_life_years": 75,
        "analysis_period_years": 150,
        "discount_rate_percent": 6.7,
        "inflation_rate_percent": 5.15,
        "interest_rate_percent": 7.75,
        "investment_ratio": 0.5,
        "social_cost_of_carbon_per_mtco2e": 86.40,
        "currency_conversion": 88.73,
        "construction_period_months": 5.2,
        "working_days_per_month": 26,
        "days_per_month": 30
    },
    "traffic_and_road_data": {
        "vehicle_data": {
            "small_cars": {"vehicles_per_day": 1405, "carbon_emissions_kgCO2e_per_km": 0.103},
            "big_cars": {"vehicles_per_day": 5502, "carbon_emissions_kgCO2e_per_km": 0.269},
            "two_wheelers": {"vehicles_per_day": 10359, "carbon_emissions_kgCO2e_per_km": 0.0351},
            "o_buses": {"vehicles_per_day": 387, "carbon_emissions_kgCO2e_per_km": 0.45483},
            "d_buses": {"vehicles_per_day": 394, "carbon_emissions_kgCO2e_per_km": 0.60644},
            "lcv": {"vehicles_per_day": 3068, "carbon_emissions_kgCO2e_per_km": 0.307},
            "hcv": {"vehicles_per_day": 1352, "carbon_emissions_kgCO2e_per_km": 0.7375, "pwr": 8},
            "mcv": {"vehicles_per_day": 119, "carbon_emissions_kgCO2e_per_km": 0.5928, "pwr": 7.22}
        },
        "accident_severity_distribution": {
            "minor": 90,
            "major": 8,
            "fatal": 2
        },
        "additional_inputs": {
            "alternate_road_carriageway": "2L",
            "carriage_width_in_m": 8,
            "road_roughness_mm_per_km": 2000,
            "road_rise_m_per_km": 0,
            "road_fall_m_per_km": 0,
            "additional_reroute_distance_km": 0.175,
            "additional_travel_time_min": 0.525,
            "crash_rate_accidents_per_million_km": 141.64,
            "work_zone_multiplier": 1.0,
            "peak_hour_traffic_percent_per_hour": [0.10, 0.10, 0.10, 0.10],
            "hourly_capacity": 1900,
            "force_free_flow_off_peak": True
        }
    },
    "maintenance_and_stage_parameters": {
        "use_stage_cost": {
            "routine": {
                "inspection": {
                    "percentage_of_initial_construction_cost_per_year": 0.1,
                    "interval_in_years": 1
                },
                "maintenance": {
                    "percentage_of_initial_construction_cost_per_year": 0.55,
                    "percentage_of_initial_carbon_emission_cost": 0.55,
                    "interval_in_years": 5
                }
            },
            "major": {
                "inspection": {
                    "percentage_of_initial_construction_cost": 0.5,
                    "interval_for_repair_and_rehabitation_in_years": 5
                },
                "repair": {
                    "percentage_of_initial_construction_cost": 10,
                    "percentage_of_initial_carbon_emission_cost": 0.55,
                    "interval_for_repair_and_rehabitation_in_years": 20,
                    "repairs_duration_months": 3
                }
            },
            "replacement_costs_for_bearing_and_expansion_joint": {
                "percentage_of_super_structure_cost": 12.5,
                "interval_of_replacement_in_years": 25,
                "duration_of_replacement_in_days": 2
            }
        },
        "end_of_life_stage_costs": {
            "demolition_and_disposal": {
                "percentage_of_initial_construction_cost": 10,
                "percentage_of_initial_carbon_emission_cost": 10,
                "duration_for_demolition_and_disposal_in_months": 1
            }
        }
    },
    
}
