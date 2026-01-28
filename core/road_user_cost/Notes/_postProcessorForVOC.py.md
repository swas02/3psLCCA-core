import VOC.utils.IRCSP302019TableC1 as tableC1
from VOC.utils.constants import vehicle_type_list, petrolToDieselRatio
import json
import os

wpiAdjustedValues = {
    "distanceCost": {},
    "timeCost": {}
}

def calculate_total_cost(data):
    """
    Calculate total cost for both distanceCost and timeCost in the data.
    Updates totals based on IT/ET or value fields.
    Returns a dictionary with both totals and vehicle-specific totals.
    """
    total_cost = {}

    for cost_type in ["distanceCost", "timeCost"]:
        if cost_type not in data:
            continue

        # Initialize the cost type (distanceCost or timeCost) structure
        total_cost[cost_type] = {"total": {"IT": 0.0, "ET": 0.0}}

        # Iterate over vehicle types (e.g., small_cars, big_cars)
        for vehicle_type, components in data[cost_type].items():
            # Skip if it's not a vehicle type (like "total" itself)
            if vehicle_type == "total":
                continue

            # Initialize each vehicle type's totals
            total_cost[cost_type][vehicle_type] = {"IT": 0.0, "ET": 0.0}

            # Iterate over each component (e.g., tyreCost, fuelCost, etc.)
            for comp_name, comp_values in components.items():
                # Skip precomputed totals to avoid double counting
                if comp_name.startswith("total_"):
                    continue

                # If the component is a dictionary (contains IT/ET values)
                if isinstance(comp_values, dict):
                    if comp_values.get('iHTC', False):
                        total_cost[cost_type]["total"]["IT"] += comp_values.get("IT", 0)
                        total_cost[cost_type]["total"]["ET"] += comp_values.get("ET", 0)
                        total_cost[cost_type][vehicle_type]["IT"] += comp_values.get("IT", 0)
                        total_cost[cost_type][vehicle_type]["ET"] += comp_values.get("ET", 0)
                    else:
                        # Add the value to both the total cost and the specific vehicle's total
                        value = comp_values.get("value", 0)
                        total_cost[cost_type]["total"]["IT"] += value
                        total_cost[cost_type]["total"]["ET"] += value
                        total_cost[cost_type][vehicle_type]["IT"] += value
                        total_cost[cost_type][vehicle_type]["ET"] += value
                # If the component is a numeric value (float or int)
                elif isinstance(comp_values, (int, float)):
                    total_cost[cost_type]["total"]["IT"] += comp_values
                    total_cost[cost_type]["total"]["ET"] += comp_values
                    total_cost[cost_type][vehicle_type]["IT"] += comp_values
                    total_cost[cost_type][vehicle_type]["ET"] += comp_values
                else:
                    # Skip unexpected types
                    continue

        # Add the units information
        total_cost[cost_type]["units"] = "Rs/km/veh"

    return total_cost



def getWPI(category, vehicle_type, wpi):
    mapping = {
        "small_cars": "Small Cars",
        "big_cars": "Big Cars",
        "two_wheelers": "Two Wheeler",
        "buses": "Ordinary Buses",
        "lcv": "LCV",
        "hcv": "HCV",
        "mcv": "MCV"
    }

    vt = mapping.get(vehicle_type)

    WPI_data = wpi["WPI"]

    # 1️⃣ CATEGORY EXISTS AT TOP LEVEL (fuelCost, commodityHoldingCost, medicalCost, passengerCrewCost, votCost)
    if category in WPI_data:
        block = WPI_data[category]

        # If it is vehicle-based return only for that vehicle type
        if isinstance(block, dict) and vt in block:
            return block[vt]

        # Otherwise return entire block (fuelCost, medicalCost, etc.)
        return block

    # 2️⃣ CATEGORY INSIDE vehicleCost (tyreCost, spareParts, fixedDepreciation, propertyDamage)
    if category in WPI_data["vehicleCost"]:
        block = WPI_data["vehicleCost"][category]

        # must be vehicle-based here
        return block.get(vt)

    return None



def post_process(outputFromVocOutputBuilder, wpi, debug=False):
    # print(outputFromVocOutputBuilder)
    for vt in vehicle_type_list:
        if vt in outputFromVocOutputBuilder:
            wpiAdjustedValues["distanceCost"][vt] = {}

    # ----------------------------------------------------------
    # PART 1 : TYRE COST PER KM
    # ----------------------------------------------------------
    for vt in vehicle_type_list:

        if vt not in outputFromVocOutputBuilder:
            continue

        vdata = outputFromVocOutputBuilder[vt]
        if "VOC_summary" not in vdata:
            continue

        tyre_life_block = vdata["VOC_summary"]["distance_related"]["tyre_life"]
        tyre_life_km = tyre_life_block["value"]

        tyre_info = tableC1.new_tyres_costs[vt]

        cost_per_tyre_wt = tyre_info["IT"]
        cost_per_tyre_wot = tyre_info["ET"]
        num_tyres = tyre_info["num_of_wheels"]

        total_cost_set_wt = num_tyres * cost_per_tyre_wt
        total_cost_set_wot = num_tyres * cost_per_tyre_wot

        tyre_cost_per_km_wt = total_cost_set_wt / tyre_life_km
        tyre_cost_per_km_wot = total_cost_set_wot / tyre_life_km

        tyre_life_block["tyre_cost_rs_per_km"] = {
            "num_tyres": num_tyres,
            "IT": tyre_cost_per_km_wt,
            "ET": tyre_cost_per_km_wot,
            "unit": "Rs/km",
            "iHTC": True
        }

        # Final Output Storage
        wpiAdjustedValues["distanceCost"][vt]["tyreCost"] = {
            "IT": tyre_cost_per_km_wt * getWPI("tyreCost", vt, wpi),
            "ET": tyre_cost_per_km_wot * getWPI("tyreCost", vt, wpi),
            "unit": "Rs/km",
            "iHTC": True
        }

    # ----------------------------------------------------------
    # PART 2 : FUEL + OILS + GREASE
    # ----------------------------------------------------------
    for vt in vehicle_type_list:

        if vt not in outputFromVocOutputBuilder:
            continue

        vdata = outputFromVocOutputBuilder[vt]
        if "VOC_summary" not in vdata:
            continue

        dist = vdata["VOC_summary"]["distance_related"]

        # ---------------------------
        # 1. FUEL
        # ---------------------------
        fuel = dist.get("fuel_consumption")

        if fuel:
            wpi_block = getWPI("fuelCost", vt, wpi)

            petrol_cost_per_km = {"IT": 0, "ET": 0}
            diesel_cost_per_km = {"IT": 0, "ET": 0}

            # Petrol
            if fuel.get("petrol", 0) > 0:
                liters_1000 = fuel["petrol"]
                pw = tableC1.petroleum_products_costs["petrol"]["IT"]
                pe = tableC1.petroleum_products_costs["petrol"]["ET"]

                petrol_cost_per_km = {
                    "IT": (liters_1000 * pw) / 1000,
                    "ET": (liters_1000 * pe) / 1000
                }

                dist["fuel_consumption"]["petrol_cost_rs_per_km"] = {
                    **petrol_cost_per_km,
                    "unit": "Rs/km",
                    "WPI": wpi_block["Petrol"],
                    "iHTC": False
                }

            # Diesel
            if fuel.get("diesel", 0) > 0:
                liters_1000 = fuel["diesel"]
                dw = tableC1.petroleum_products_costs["diesel"]["IT"]
                de = tableC1.petroleum_products_costs["diesel"]["ET"]

                diesel_cost_per_km = {
                    "IT": (liters_1000 * dw) / 1000,
                    "ET": (liters_1000 * de) / 1000,
                }

                dist["fuel_consumption"]["diesel_cost_rs_per_km"] = {
                    **diesel_cost_per_km,
                    "unit": "Rs/km",
                    "WPI": wpi_block["Diesel"],
                    "iHTC": False
                }

            ratio = petrolToDieselRatio.get(vt, {"petrol": 0, "diesel": 0})

            wt = ratio["petrol"] * petrol_cost_per_km["IT"] + ratio["diesel"] * diesel_cost_per_km["IT"]
            wot = ratio["petrol"] * petrol_cost_per_km["ET"] + ratio["diesel"] * diesel_cost_per_km["ET"]

            dist["fuel_consumption"]["fuel_cost_rs_per_km_final"] = {
                "IT": wt,
                "ET": wot,
                "unit": "Rs/km",
                "iHTC": False
            }

            # Final Output
            wpiAdjustedValues["distanceCost"][vt]["fuelCost"] = {
                "IT": ratio["petrol"] * petrol_cost_per_km["IT"] * wpi_block["Petrol"] +
                      ratio["diesel"] * diesel_cost_per_km["IT"] * wpi_block["Diesel"],
                "ET": ratio["petrol"] * petrol_cost_per_km["ET"] * wpi_block["Petrol"] +
                      ratio["diesel"] * diesel_cost_per_km["ET"] * wpi_block["Diesel"],
                "unit": "Rs/km",
                "iHTC": True
            }

        # ---------------------------
        # 2. ENGINE OIL
        # ---------------------------
        if "engine_oil" in dist:
            liters_1000 = dist["engine_oil"]["value"]

            pw = tableC1.petroleum_products_costs["engine_oil"]["IT"]
            pe = tableC1.petroleum_products_costs["engine_oil"]["ET"]

            IT = (liters_1000 * pw) / 1000
            ET = (liters_1000 * pe) / 1000

            dist["engine_oil"]["engine_oil_cost_rs_per_km"] = {
                "IT": IT,
                "ET": ET,
                "unit": "Rs/km",
                "WPI": getWPI("fuelCost", vt, wpi)["Engine Oil"],
                "iHTC": True
            }

            wpiAdjustedValues["distanceCost"][vt]["engine_oil"] = {
                "IT": IT * getWPI("fuelCost", vt, wpi)["Engine Oil"],
                "ET": ET * getWPI("fuelCost", vt, wpi)["Engine Oil"],
                "unit": "Rs/km",
                "iHTC": True
            }

        # ---------------------------
        # 3. OTHER OIL
        # ---------------------------
        if "other_oil" in dist:
            liters_10000 = dist["other_oil"]["value"]

            pw = tableC1.petroleum_products_costs["other_oil"]["IT"]
            pe = tableC1.petroleum_products_costs["other_oil"]["ET"]

            IT = (liters_10000 * pw) / 10000
            ET = (liters_10000 * pe) / 10000

            dist["other_oil"]["other_oil_cost_rs_per_km"] = {
                "IT": IT,
                "ET": ET,
                "unit": "Rs/km",
                "WPI": getWPI("fuelCost", vt, wpi)["Other Oil"],
                "iHTC": True
            }

            wpiAdjustedValues["distanceCost"][vt]["other_oil"] = {
                "IT": IT * getWPI("fuelCost", vt, wpi)["Other Oil"],
                "ET": ET * getWPI("fuelCost", vt, wpi)["Other Oil"],
                "unit": "Rs/km",
                "iHTC": True
            }

        # ---------------------------
        # 4. GREASE
        # ---------------------------
        if "grease" in dist:
            liters_10000 = dist["grease"]["value"]

            pw = tableC1.petroleum_products_costs["grease"]["IT"]
            pe = tableC1.petroleum_products_costs["grease"]["ET"]

            IT = (liters_10000 * pw) / 10000
            ET = (liters_10000 * pe) / 10000

            dist["grease"]["grease_cost_rs_per_km"] = {
                "IT": IT,
                "ET": ET,
                "unit": "Rs/km",
                "WPI": getWPI("fuelCost", vt, wpi)["Grease"],
                "iHTC": True
            }

            wpiAdjustedValues["distanceCost"][vt]["grease"] = {
                "IT": IT * getWPI("fuelCost", vt, wpi)["Grease"],
                "ET": ET * getWPI("fuelCost", vt, wpi)["Grease"],
                "unit": "Rs/km",
                "iHTC": True
            }

        # ---------------------------
        # 5. SPARE PARTS + Maintenance Labour 
        # ---------------------------

        # Spare Parts
        if "spare_parts" in dist:
            dist["spare_parts"]["WPI"] = getWPI("spareParts", vt, wpi)
            wpiAdjustedValues["distanceCost"][vt]["spare_parts"] = {
                "IT": dist["spare_parts"]["IT"] * getWPI("spareParts", vt, wpi),
                "ET": dist["spare_parts"]["ET"] * getWPI("spareParts", vt, wpi),
                "unit": "Rs/km",
                "iHTC": True
            }

        # Maintenance Labour is dependent on spare parts price
        if "maintenance_labour" in dist:
            dist["maintenance_labour"]["WPI"] = getWPI("spareParts", vt, wpi)
            wpiAdjustedValues["distanceCost"][vt]["maintenance_labour"] = {
                "value": dist["maintenance_labour"]["value"] * getWPI("spareParts", vt, wpi),
                "unit": "Rs/km",
                "iHTC": False
            }



        if "VOC_summary" not in vdata or "time_related" not in vdata["VOC_summary"]:
            continue

        time_block = vdata["VOC_summary"]["time_related"]

        # Initialize dict for this vehicle type
        wpiAdjustedValues["timeCost"][vt] = {}

        # 1. Fixed cost
        if "fixed_cost" in time_block:
            time_block["fixed_cost"]["WPI"] = getWPI("fixedDepreciation", vt, wpi)
            wpiAdjustedValues["timeCost"][vt]["fixed_cost"] = {
                "IT": time_block["fixed_cost"]["IT"] * getWPI("fixedDepreciation", vt, wpi),
                "ET": time_block["fixed_cost"]["ET"] * getWPI("fixedDepreciation", vt, wpi),
                "unit": "Rs/km",
                "iHTC": time_block["fixed_cost"]["iHTC"]
            }

        # 2. Depreciation cost
        if "depreciation_cost" in time_block:
            time_block["depreciation_cost"]["WPI"] = getWPI("fixedDepreciation", vt, wpi)
            wpiAdjustedValues["timeCost"][vt]["depreciation_cost"] = {
                "IT": time_block["depreciation_cost"]["IT"] * getWPI("fixedDepreciation", vt, wpi),
                "ET": time_block["depreciation_cost"]["ET"] * getWPI("fixedDepreciation", vt, wpi),
                "unit": time_block["depreciation_cost"]["unit"],
                "iHTC": time_block["depreciation_cost"]["iHTC"]
            }

        # 3. Passenger time cost
        if "passenger_time_cost" in time_block:
            pc_WPI = getWPI("passengerCrewCost", vt, wpi)["Passenger Cost"]
            time_block["passenger_time_cost"]["WPI"] = pc_WPI
            wpiAdjustedValues["timeCost"][vt]["passenger_time_cost"] = {
                "value": time_block["passenger_time_cost"]["value"] * pc_WPI,
                "unit": time_block["passenger_time_cost"]["unit"],
                "iHTC": time_block["passenger_time_cost"]["iHTC"]
            }

        # 4. Crew cost
        if "crew_cost" in time_block:
            cc_WPI = getWPI("passengerCrewCost", vt, wpi)["Crew Cost"]
            time_block["crew_cost"]["WPI"] = cc_WPI
            wpiAdjustedValues["timeCost"][vt]["crew_cost"] = {
                "value": time_block["crew_cost"]["value"] * cc_WPI,
                "unit": "Rs/km",
                "iHTC": time_block["crew_cost"]["iHTC"]
            }

        # 5. Commodity holding cost
        if "commodity_holding_cost" in time_block:
            chc_wpi = getWPI("commodityHoldingCost", vt, wpi)
            time_block["commodity_holding_cost"]["WPI"] = chc_wpi
            wpiAdjustedValues["timeCost"][vt]["commodity_holding_cost"] = {
                "value": time_block["commodity_holding_cost"]["value"] * chc_wpi,
                "unit": "Rs/km",
                "iHTC": time_block["commodity_holding_cost"]["iHTC"]
            }
        

        # 6. Total time cost
        total_IT = 0
        total_ET = 0
        for key, cost in wpiAdjustedValues["timeCost"][vt].items():
            if "IT" in cost:
                total_IT += cost["IT"]
            if "ET" in cost:
                total_ET += cost["ET"]
            if "value" in cost:
                total_IT += cost["value"]
                total_ET += cost["value"]

        wpiAdjustedValues["timeCost"][vt]["total_time_cost"] = {
            "IT": total_IT,
            "ET": total_ET,
            "unit": "Rs/km",
            "iHTC": True
        }
    summaryOfVOC = calculate_total_cost(wpiAdjustedValues)




    if debug:
        # Ensure debug folder exists
        os.makedirs("debug", exist_ok=True)
        # Save each output separately
        json.dump(outputFromVocOutputBuilder, open("debug/outputFromVocOutputBuilder.json", "w"), indent=4)
        json.dump(wpiAdjustedValues, open("debug/wpiAdjustedValues.json", "w"), indent=4)
        json.dump(summaryOfVOC, open("debug/summaryOfVOC.json", "w"), indent=4)


    return summaryOfVOC
