from .... import standard_keys as c
vehicle_type_list = [c.SMALL_CARS, c.BIG_CARS, c.TWO_WHEELERS, c.BUSES, c.LCV, c.HCV, c.MCV]

petrolToDieselRatio = {
    c.SMALL_CARS: {
        c.PETROL: 0.7,
        c.DIESEL: 0.3
    },
    c.BIG_CARS: {
        c.PETROL: 0.3,
        c.DIESEL: 0.7
    },
    c.TWO_WHEELERS: {
        c.PETROL: 1,
        c.DIESEL: 0
    },
    c.BUSES: {
        c.PETROL: 0,
        c.DIESEL: 1
    },
    c.LCV: {
        c.PETROL: 0,
        c.DIESEL: 1
    },
    c.HCV: {
        c.PETROL: 0,
        c.DIESEL: 1
    },
    c.MCV: {
        c.PETROL: 0,
        c.DIESEL: 1
    },
}


pcu = {
    c.SMALL_CARS: 1, 
    c.BIG_CARS: 1, 
    c.TWO_WHEELERS: 0.75, 
    c.BUSES: 2.2, 
    c.LCV: 1.4, 
    c.HCV: 2.2, 
    c.MCV: 2.2
}