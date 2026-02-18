from dataclasses import dataclass, asdict
from typing import Dict

@dataclass(frozen=True)
class FuelCost:
    petrol: float
    diesel: float
    engine_oil: float
    other_oil: float
    grease: float


@dataclass(frozen=True)
class VehicleCategoryCost:
    small_cars: float
    big_cars: float
    two_wheelers: float
    o_buses: float
    d_buses: float
    lcv: float
    hcv: float
    mcv: float


@dataclass(frozen=True)
class VehicleCost:
    property_damage: VehicleCategoryCost
    tyre_cost: VehicleCategoryCost
    spare_parts: VehicleCategoryCost
    fixed_depreciation: VehicleCategoryCost

@dataclass(frozen=True)
class CommodityHoldingCost(VehicleCategoryCost):
    pass

@dataclass(frozen=True)
class VOTCost(VehicleCategoryCost):
    pass

@dataclass(frozen=True)
class PassengerCrewCost:
    passenger_cost: float
    crew_cost: float


@dataclass(frozen=True)
class MedicalCost:
    fatal: float
    major: float
    minor: float


@dataclass(frozen=True)
class WPIBlock:
    fuel_cost: FuelCost
    vehicle_cost: VehicleCost
    commodity_holding_cost: CommodityHoldingCost
    passenger_crew_cost: PassengerCrewCost
    medical_cost: MedicalCost
    vot_cost: VOTCost


@dataclass(frozen=True)
class WPIMetaData:
    year: int
    wpi: WPIBlock

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            year=data["year"],
            wpi=WPIBlock(
                fuel_cost=FuelCost(**data["WPI"]["fuelCost"]),
                vehicle_cost=VehicleCost(
                    property_damage=VehicleCategoryCost(**data["WPI"]["vehicleCost"]["propertyDamage"]),
                    tyre_cost=VehicleCategoryCost(**data["WPI"]["vehicleCost"]["tyreCost"]),
                    spare_parts=VehicleCategoryCost(**data["WPI"]["vehicleCost"]["spareParts"]),
                    fixed_depreciation=VehicleCategoryCost(**data["WPI"]["vehicleCost"]["fixedDepreciation"]),
                ),
                commodity_holding_cost=CommodityHoldingCost(**data["WPI"]["commodityHoldingCost"]),
                passenger_crew_cost=PassengerCrewCost(
                    passenger_cost=data["WPI"]["passengerCrewCost"]["Passenger Cost"],
                    crew_cost=data["WPI"]["passengerCrewCost"]["Crew Cost"],
                ),
                medical_cost=MedicalCost(**data["WPI"]["medicalCost"]),
                vot_cost=VOTCost(**data["WPI"]["votCost"]),
            )
        )
