# IRC SP-30:2019, Table C.1 Current Vehicle Operating Cost Inputs
from .... import standard_keys as c

vehicle_costs = {
    c.TWO_WHEELERS: {c.ET: 34209, c.IT: 61235},
    c.SMALL_CARS: {c.ET: 273728, c.IT: 489972},
    c.BIG_CARS: {c.ET: 558599, c.IT: 999892},
    c.BUSES: {c.ET: 1647150, c.IT: 2948400},
    c.LCV: {c.ET: 449721, c.IT: 805000},
    c.HCV: {c.ET: 940531, c.IT: 1683550},
    c.MCV: {c.ET: 1415350, c.IT: 1415350},
}

petroleum_products_costs = {
    c.PETROL: {
        c.ET: 33.58,
        c.IT: 79.92,
        c.UNITS: "Rs/l"
    },
    c.DIESEL: {
        c.ET: 30.51,
        c.IT: 72.61,
        c.UNITS: "Rs/l"
    },
    c.ENGINE_OIL: {
        c.ET: 187.96,
        c.IT: 384.39,
        c.UNITS: "Rs/l"
    },
    c.OTHER_OIL: {
        c.ET: 167.70,
        c.IT: 338.78,
        c.UNITS: "Rs/l"
    },
    c.GREASE: {
        c.ET: 183.70,
        c.IT: 390.90,
        c.UNITS: "Rs/kg"
    }
}

new_tyres_costs = {
    c.TWO_WHEELERS: {
        c.ET: 1355,
        c.IT: 1668,
        c.UNITS: "Rs/unit",
        c.NUMBER_OF_WHEELS: 2  # Source "Steel - reconstruction, inflation included" sheets
    },
    c.BIG_CARS: {
        c.ET: 2940,
        c.IT: 4456,
        c.UNITS: "Rs/unit",
        c.NUMBER_OF_WHEELS: 4  # Source "Steel - reconstruction, inflation included" sheets
    },
    c.SMALL_CARS: {
        c.ET: 2940,
        c.IT: 4456,
        c.UNITS: "Rs/unit",
        c.NUMBER_OF_WHEELS: 4  # Source "Steel - reconstruction, inflation included" sheets
    },
    c.BUSES: {
        c.ET: 13475,
        c.IT: 17500,
        c.UNITS: "Rs/unit",
        c.NUMBER_OF_WHEELS: 6  # Source "Steel - reconstruction, inflation included" sheets
    },
    c.LCV: {
        c.ET: 5420,
        c.IT: 8900,
        c.UNITS: "Rs/unit",
        c.NUMBER_OF_WHEELS: 6  # Source "Steel - reconstruction, inflation included" sheets
    },
    c.HCV: {
        c.ET: 13890,
        c.IT: 20000,
        c.UNITS: "Rs/unit",
        c.NUMBER_OF_WHEELS: 10  # Source "Steel - reconstruction, inflation included" sheets
    },
    c.MCV: {
        c.ET: 13890,
        c.IT: 20000,
        c.UNITS: "Rs/unit",
        c.NUMBER_OF_WHEELS: 14  # Source "Steel - reconstruction, inflation included" sheets
    }
}
