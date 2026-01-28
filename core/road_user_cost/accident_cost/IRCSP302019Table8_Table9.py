from ... import standard_keys as c


def table8_Economic_Cost_for_Different_Type_of_Accidents():
    """
    Returns economic cost (INR) for different accident severities
    as per Table 8.
    """
    return {
        c.FATAL: 1325049,
        c.MAJOR: 432651,
        c.MINOR: 46680
    }


def table9_Economic_Cost_of_Quantum_of_Vehicle_Damage_due_to_Accidents():
    """
    Returns economic cost (INR) of vehicle damage due to accidents
    for different vehicle types as per Table 9.
    """
    return {
        c.SMALL_CARS: 40088,
        c.BIG_CARS: 40088,
        c.TWO_WHEELERS: 11651,
        c.O_BUSES: 116585,
        c.LCV: 120494,
        c.HCV: 120494,
        c.MCV: 205483
    }
