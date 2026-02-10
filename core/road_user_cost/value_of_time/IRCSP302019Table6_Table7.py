from ... import standard_keys as c
def valueofTravelTime(lane_type):
    """
    Returns the Value of Travel Time (Rs./hour) for different vehicle types
    based on the specified lane type.

    Parameters:
        lane_type (str): Type of carriageway/lane.
            Valid values: "SL", "IL", "2L", "4L", "6L", "8L", "EW"

    Returns:
        dict: A dictionary mapping vehicle types to their corresponding
        value of travel time (Rs./hour).

    Data Source:
        IRC:SP:30-2019 — Table 6 and Table 7

    Notes:
        1. 'o_buses' refers to Ordinary Buses and 'd_buses' refers to Deluxe Buses.
        2. For "Value of Commodity on Different Types of Carriageways"
        (IRC SP 30-2019, Table 7), the returned values for LCV, HCV,
        and MCV represent "commodity holding cost" and are originally
        specified in **Rs./day**.
    """

    if lane_type in [c.SL, c.IL]:
        return {
            c.SMALL_CARS: 98.5,
            c.BIG_CARS: 98.5,
            c.TWO_WHEELERS: 41.3,
            c.O_BUSES: 27.2,
            c.D_BUSES: 0,
            c.LCV: 101.6 / 24,
            c.HCV: 278.8 / 24,
            c.MCV: 0
        }

    elif lane_type == "2L":
        return {
            c.SMALL_CARS: 117.30,
            c.BIG_CARS: 117.30,
            c.TWO_WHEELERS: 60.10,
            c.O_BUSES: 73.20,
            c.D_BUSES: 81.60,
            c.LCV: 109.5 / 24,
            c.HCV: 333.6 / 24,
            c.MCV: 625.4 / 24
        }

    elif lane_type in [c.L4, c.L6, c.L8, c.EW]:
        return {
            c.SMALL_CARS: 0,
            c.BIG_CARS: 0,
            c.TWO_WHEELERS: 0,
            c.O_BUSES: 0,
            c.D_BUSES: 0,
            c.LCV: 228 / 24,
            c.HCV: 1654.8 / 24,
            c.MCV: 2606 / 24
        }

    else:
        raise ValueError("Unknown lane type")



def average_occupancy():
    """
    Returns the average vehicle occupancy for different vehicle types.

    Returns:
        dict: A dictionary with vehicle types as keys and their
        corresponding average occupancy (persons/vehicle) as values.

    Notes:
        1. 'o_buses' refers to Ordinary Buses and 'd_buses' refers to Deluxe Buses.
        2. Values are average number of passengers per vehicle.
    """

    return {
        c.SMALL_CARS: 3.23,
        c.BIG_CARS: 4.28,
        c.TWO_WHEELERS: 1.71,
        c.O_BUSES: 30.0,
        c.D_BUSES: 40.0
    }
