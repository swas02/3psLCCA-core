import json
from three_ps_lcca_core.inputs.wpi import (
    WPIMetaData,
    WPIBlock,
    FuelCost,
    VehicleCost,
    VehicleCategoryCost,
    CommodityHoldingCost,
    PassengerCrewCost,
    MedicalCost,
    VOTCost,
)

wpi_object = WPIMetaData(
    year=2024,
    wpi=WPIBlock(
        fuel_cost=FuelCost(
            petrol=1.8067915690866512,
            diesel=1.7733050847457628,
            engine_oil=1.4496951219512195,
            other_oil=1.6951351351351354,
            grease=1.6951351351351354,
        ),
        vehicle_cost=VehicleCost(
            property_damage=VehicleCategoryCost(
                1.1395759717314486,
                1.1395759717314486,
                1.1395759717314486,
                1.1395759717314486,
                1.1395759717314486,
                1.1395759717314486,
                1.1395759717314486,
                1.1395759717314486,
            ),
            tyre_cost=VehicleCategoryCost(
                1.123991935483871,
                1.123991935483871,
                1.1336538461538461,
                1.1702564102564101,
                1.1702564102564101,
                1.1702564102564101,
                1.1702564102564101,
                1.1702564102564101,
            ),
            spare_parts=VehicleCategoryCost(
                1.1395759717314486,
                1.1395759717314486,
                1.1395759717314486,
                1.1395759717314486,
                1.1395759717314486,
                1.1395759717314486,
                1.1395759717314486,
                1.1395759717314486,
            ),
            fixed_depreciation=VehicleCategoryCost(
                1.1388400702987698,
                1.1388400702987698,
                1.1388400702987698,
                1.1388400702987698,
                1.1388400702987698,
                1.1388400702987698,
                1.1388400702987698,
                1.1388400702987698,
            ),
        ),
        commodity_holding_cost=CommodityHoldingCost(
            1.4788593903638152,
            1.4788593903638152,
            1.4788593903638152,
            1.4788593903638152,
            1.4788593903638152,
            1.4788593903638152,
            1.4788593903638152,
            1.4788593903638152,
        ),
        passenger_crew_cost=PassengerCrewCost(
            passenger_cost=1.2706270627062706,
            crew_cost=1.2706270627062706,
        ),
        medical_cost=MedicalCost(
            fatal=1.0867924528301887,
            major=1.0867924528301887,
            minor=1.0867924528301887,
        ),
        vot_cost=VOTCost(
            1.2706270627062706,
            1.2706270627062706,
            1.2706270627062706,
            1.2706270627062706,
            1.2706270627062706,
            1.2706270627062706,
            1.2706270627062706,
            1.2706270627062706,
        ),
    ),
)

wpi = wpi_object.to_dict()

# python -m examples.from_metadata.wpi
if __name__ == "__main__":
    print(json.dumps(wpi, indent=4))
