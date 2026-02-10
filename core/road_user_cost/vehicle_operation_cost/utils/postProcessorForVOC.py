from ..utils import IRCSP302019TableC1 as tableC1
from ..utils.constants import vehicle_type_list, petrolToDieselRatio
from typing import Any, Dict, Optional, Union
from .... import standard_keys as c
from ....utils.dump_to_file import dump_to_file


def calculate_total_cost(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate total cost for both distanceCost and timeCost in the data.
    Updates totals based on IT/ET or value fields.
    Returns a dictionary with both totals and vehicle-specific totals.
    """
    total_cost: Dict[str, Any] = {}

    for cost_type in ["distanceCost", "timeCost"]:
        if cost_type not in data:
            continue

        # total_cost[cost_type] = {"total": {c.IT: 0.0, c.ET: 0.0}}
        total_cost[cost_type] = {}


        for vehicle_type, components in data[cost_type].items():
            if vehicle_type == "total":
                continue

            total_cost[cost_type][vehicle_type] = {c.IT: 0.0, c.ET: 0.0}

            for comp_name, comp_values in components.items():
                if comp_name.startswith("total_"):
                    continue

                if isinstance(comp_values, dict):
                    if comp_values.get('iHTC', False):
                        # total_cost[cost_type]["total"][c.IT] += comp_values.get(c.IT)
                        # total_cost[cost_type]["total"][c.ET] += comp_values.get(c.ET)
                        total_cost[cost_type][vehicle_type][c.IT] += comp_values.get(c.IT)
                        total_cost[cost_type][vehicle_type][c.ET] += comp_values.get(c.ET)
                    else:
                        value = comp_values.get(c.VALUE)
                        # total_cost[cost_type]["total"][c.IT] += value
                        # total_cost[cost_type]["total"][c.ET] += value
                        total_cost[cost_type][vehicle_type][c.IT] += value
                        total_cost[cost_type][vehicle_type][c.ET] += value
                elif isinstance(comp_values, (int, float)):
                    # total_cost[cost_type]["total"][c.IT] += comp_values
                    # total_cost[cost_type]["total"][c.ET] += comp_values
                    total_cost[cost_type][vehicle_type][c.IT] += comp_values
                    total_cost[cost_type][vehicle_type][c.ET] += comp_values
                else:
                    continue

        total_cost[cost_type][c.UNITS] = "Rs/km/veh"

    return total_cost


def getWPI(category, vehicle_type, wpi):
    WPI_data = wpi.get("WPI", {})

    # Special handling for "buses" vehicle type, use "o_buses"
    if vehicle_type == c.BUSES:
        vehicle_type = c.O_BUSES

    # 1️⃣ CATEGORY EXISTS AT TOP LEVEL (fuelCost, commodityHoldingCost, medicalCost, passengerCrewCost, votCost)
    if category in WPI_data:
        block = WPI_data[category]

        if isinstance(block, dict) and vehicle_type in block:
            return block[vehicle_type]

        return block  # entire block if not vehicle-specific

    # 2️⃣ CATEGORY INSIDE vehicleCost (tyreCost, spareParts, fixedDepreciation, propertyDamage)
    vehicle_cost = WPI_data.get("vehicleCost", {})
    if category in vehicle_cost:
        block = vehicle_cost[category]
        return block.get(vehicle_type)

    # Category not found
    raise ValueError(f"WPI category '{category}' not found for vehicle type '{vehicle_type}'.")



# ----------------- Helper functions -----------------

def per_km_cost(liters_per_unit: float, price_IT: float, price_ET: float, factor: float = 1000.0):
    IT = (liters_per_unit * price_IT) / factor
    ET = (liters_per_unit * price_ET) / factor
    return IT, ET


def apply_wpi(cost: Dict[str, float], wpi_val: Union[float, Dict[str, Any], None]) -> dict[str, float | str | bool]:
    # normalize wpi_val to a numeric multiplier
    multiplier: float = 1.0
    if isinstance(wpi_val, (int, float)):
        multiplier = float(wpi_val)
    elif isinstance(wpi_val, dict):
        # prefer common numeric keys
        if c.IT in wpi_val and isinstance(wpi_val[c.IT], (int, float)):
            multiplier = float(wpi_val[c.IT])
        elif c.VALUE in wpi_val and isinstance(wpi_val[c.VALUE], (int, float)):
            multiplier = float(wpi_val[c.VALUE])
        else:
            # try to pick any numeric value from the dict
            for v in wpi_val.values():
                if isinstance(v, (int, float)):
                    multiplier = float(v)
                    break

    return {
        c.IT: cost[c.IT] * multiplier,
        c.ET: cost[c.ET] * multiplier,
        c.UNIT: "Rs/km",
        c.iHTC: True
    }


# ----------------- Main function -----------------

def post_process(outputFromVocOutputBuilder: Dict[str, Any], wpi: Dict[str, Any], debug: bool = False) -> Dict[str, Any]:
    wpiAdjustedValues: Dict[str, Any] = {"distanceCost": {}, "timeCost": {}}

    for vt in vehicle_type_list:
        if vt in outputFromVocOutputBuilder:
            wpiAdjustedValues["distanceCost"][vt] = {}

    # ---------------- TYRE COST ----------------
    for vt in vehicle_type_list:
        vdata = outputFromVocOutputBuilder.get(vt)
        if not vdata or "VOC_summary" not in vdata:
            continue

        tyre_life_km = vdata["VOC_summary"]["distance_related"]["tyre_life"][c.VALUE]
        tyre_info = tableC1.new_tyres_costs[vt]

        IT, ET = tyre_info[c.IT], tyre_info[c.ET]
        num_tyres = tyre_info[c.NUMBER_OF_WHEELS]

        tyre_cost_per_km_wt = IT * num_tyres / tyre_life_km
        tyre_cost_per_km_wot = ET * num_tyres / tyre_life_km

        vdata["VOC_summary"]["distance_related"]["tyre_life"]["tyre_cost_rs_per_km"] = {
            c.NUMBER_OF_WHEELS: num_tyres,
            c.IT: tyre_cost_per_km_wt,
            c.ET: tyre_cost_per_km_wot,
            c.UNIT: "Rs/km",
            c.iHTC: True
        }

        wpi_val = getWPI("tyreCost", vt, wpi)
        wpiAdjustedValues["distanceCost"][vt]["tyreCost"] = apply_wpi(
            {c.IT: tyre_cost_per_km_wt, c.ET: tyre_cost_per_km_wot}, wpi_val
        )

    # ---------------- FUEL, OILS, GREASE ----------------
    for vt in vehicle_type_list:
        vdata = outputFromVocOutputBuilder.get(vt)
        if not vdata or "VOC_summary" not in vdata:
            continue

        dist = vdata["VOC_summary"]["distance_related"]
        wpiAdjustedValues["distanceCost"].setdefault(vt, {})

        # Fuel
        fuel = dist.get("fuel_consumption")
        if fuel:
            wpi_block = getWPI("fuelCost", vt, wpi)

            petrol_cost = {c.IT: 0, c.ET: 0}
            diesel_cost = {c.IT: 0, c.ET: 0}

            if fuel.get(c.PETROL) > 0:
                liters_1000 = fuel[c.PETROL]
                pw = tableC1.petroleum_products_costs[c.PETROL][c.IT]
                pe = tableC1.petroleum_products_costs[c.PETROL][c.ET]
                petrol_cost[c.IT], petrol_cost[c.ET] = per_km_cost(liters_1000, pw, pe) # type: ignore
                fuel["petrol_cost_rs_per_km"] = {
                    **petrol_cost, c.UNIT: "Rs/km", "WPI": wpi_block.get(c.PETROL), c.iHTC: False
                }

            if fuel.get(c.DIESEL) > 0:
                liters_1000 = fuel[c.DIESEL]
                dw = tableC1.petroleum_products_costs[c.DIESEL][c.IT]
                de = tableC1.petroleum_products_costs[c.DIESEL][c.ET]
                diesel_cost[c.IT], diesel_cost[c.ET] = per_km_cost(liters_1000, dw, de) # type: ignore
                fuel["diesel_cost_rs_per_km"] = {
                    **diesel_cost, c.UNIT: "Rs/km", "WPI": wpi_block.get(c.DIESEL), c.iHTC: False
                }

            ratio = petrolToDieselRatio.get(vt, {c.PETROL: 0, c.DIESEL: 0})
            wt = ratio[c.PETROL] * petrol_cost[c.IT] + ratio[c.DIESEL] * diesel_cost[c.IT]
            wot = ratio[c.PETROL] * petrol_cost[c.ET] + ratio[c.DIESEL] * diesel_cost[c.ET]

            fuel["fuel_cost_rs_per_km_final"] = {c.IT: wt, c.ET: wot, c.UNIT: "Rs/km", c.iHTC: False}
            wpiAdjustedValues["distanceCost"][vt]["fuelCost"] = {
                c.IT: ratio[c.PETROL] * petrol_cost[c.IT] * wpi_block.get(c.PETROL) +
                      ratio[c.DIESEL] * diesel_cost[c.IT] * wpi_block.get(c.DIESEL),
                c.ET: ratio[c.PETROL] * petrol_cost[c.ET] * wpi_block.get(c.PETROL) +
                      ratio[c.DIESEL] * diesel_cost[c.ET] * wpi_block.get(c.DIESEL),
                c.UNIT: "Rs/km",
                c.iHTC: True
            }

        # Engine oil, other oil, grease
        for oil_name in [c.ENGINE_OIL, c.OTHER_OIL, c.GREASE]:
            if oil_name in dist:
                liters = dist[oil_name][c.VALUE]
                factor = 1000 if oil_name == c.ENGINE_OIL else 10000
                pw = tableC1.petroleum_products_costs[oil_name][c.IT]
                pe = tableC1.petroleum_products_costs[oil_name][c.ET]
                IT, ET = per_km_cost(liters, pw, pe, factor)

                wpi_val = getWPI("fuelCost", vt, wpi)
                if isinstance(wpi_val, dict):
                    wpi_val = wpi_val.get(oil_name)
                else:
                    wpi_val = 1.0

                dist[oil_name][f"{oil_name}_cost_rs_per_km"] = {c.IT: IT, c.ET: ET, c.UNIT: "Rs/km", "WPI": wpi_val, c.iHTC: True}
                wpiAdjustedValues["distanceCost"][vt][oil_name] = apply_wpi({c.IT: IT, c.ET: ET}, wpi_val)

        # Spare parts and maintenance labour
        if c.SP in dist:
            wpi_val = getWPI("spareParts", vt, wpi)
            dist[c.SP]["WPI"] = wpi_val
            wpiAdjustedValues["distanceCost"][vt][c.SP] = {
                c.IT: dist[c.SP][c.IT] * wpi_val,
                c.ET: dist[c.SP][c.ET] * wpi_val,
                c.UNIT: "Rs/km",
                c.iHTC: True
            }

        if "maintenance_labour" in dist:
            wpi_val = getWPI("spareParts", vt, wpi)
            dist["maintenance_labour"]["WPI"] = wpi_val
            wpiAdjustedValues["distanceCost"][vt]["maintenance_labour"] = {
                c.VALUE: dist["maintenance_labour"][c.VALUE] * wpi_val,
                c.UNIT: "Rs/km",
                c.iHTC: False
            }

        # ---------------- TIME COST ----------------
        if "time_related" not in vdata["VOC_summary"]:
            continue

        time_block = vdata["VOC_summary"]["time_related"]
        wpiAdjustedValues["timeCost"][vt] = {}

        # Fixed and depreciation cost
        for key in ["fixed_cost", "depreciation_cost"]:
            if key in time_block:
                wpi_val = getWPI("fixedDepreciation", vt, wpi)
                time_block[key]["WPI"] = wpi_val
                wpiAdjustedValues["timeCost"][vt][key] = {
                    c.IT: time_block[key][c.IT] * wpi_val,
                    c.ET: time_block[key][c.ET] * wpi_val,
                    c.UNIT: time_block[key][c.UNIT],
                    c.iHTC: time_block[key][c.iHTC]
                }

        # Passenger and crew cost
        for key, sub_key in [("passenger_time_cost", "Passenger Cost"), ("crew_cost", "Crew Cost")]:
            if key in time_block:
                wpi_val = getWPI("passengerCrewCost", vt, wpi).get(sub_key)
                time_block[key]["WPI"] = wpi_val
                wpiAdjustedValues["timeCost"][vt][key] = {
                    c.VALUE: time_block[key][c.VALUE] * wpi_val,
                    c.UNIT: time_block[key][c.UNIT],
                    c.iHTC: time_block[key][c.iHTC]
                }

        # Commodity holding cost
        if "commodity_holding_cost" in time_block:
            wpi_val = getWPI("commodityHoldingCost", vt, wpi)
            time_block["commodity_holding_cost"]["WPI"] = wpi_val
            wpiAdjustedValues["timeCost"][vt]["commodity_holding_cost"] = {
                c.VALUE: time_block["commodity_holding_cost"][c.VALUE] * wpi_val,
                c.UNIT: "Rs/km",
                c.iHTC: time_block["commodity_holding_cost"][c.iHTC]
            }

        # Total time cost
        total_IT, total_ET = 0, 0
        for cost in wpiAdjustedValues["timeCost"][vt].values():
            if c.IT in cost:
                total_IT += cost[c.IT]
            if c.ET in cost:
                total_ET += cost[c.ET]
            if c.VALUE in cost:
                total_IT += cost[c.VALUE]
                total_ET += cost[c.VALUE]

        wpiAdjustedValues["timeCost"][vt]["total_time_cost"] = {
            c.IT: total_IT,
            c.ET: total_ET,
            c.UNIT: "Rs/km",
            c.iHTC: True
        }

    summaryOfVOC = calculate_total_cost(wpiAdjustedValues)

    if debug:
        dump_to_file("ruc-voc-1-VOC_values_calculated_as_per_IRC_SP_30.json", outputFromVocOutputBuilder)
        dump_to_file("ruc-voc-2-VOC_values_adjusted_according_to_WPI.json", wpiAdjustedValues)
        dump_to_file("ruc-voc-3_VOC_summary.json", summaryOfVOC)
        
    return summaryOfVOC
