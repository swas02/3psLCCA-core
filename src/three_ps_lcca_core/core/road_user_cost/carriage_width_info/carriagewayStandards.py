from dataclasses import dataclass
from types import MappingProxyType
from typing import Optional, Tuple, List, Union
from ... import standard_keys as c


@dataclass(frozen=True)
class CarriagewayStandards:
    """
    Manages standard carriageway widths for different road types.
    """

    # Single structured data source
    _DATA = MappingProxyType(
        {
            # --- Undivided / Standard Roads ---
            c.SL: {
                "code": c.SL,
                "name": "Single Lane",
                "width": 3.75,
                "capacity": 435,
                "velocity_class": c.SL,
            },
            c.IL: {
                "code": c.IL,
                "name": "Intermediate Lane",
                "width": 5.50,
                "capacity": 1158,
                "velocity_class": c.IL,
            },
            c.L2: {
                "code": c.L2,
                "name": "Two Lane (Two Way)",
                "width": 7.00,
                "capacity": 2400,
                "velocity_class": c.L2,
            },
            c.L2_1W: {
                "code": c.L2_1W,
                "name": "Two Lane (One Way)",
                "width": 7.00,
                "capacity": 2700,
                "velocity_class": c.L4,
            },
            c.L3_1W: {
                "code": c.L3_1W,
                "name": "Three Lane (One Way)",
                "width": 10.50,
                "capacity": 4200,
                "velocity_class": c.L6,
            },
            c.L4: {
                "code": c.L4,
                "name": "Four Lane (Two Way)",
                "width": 7.00,
                "capacity": 5400,
                "velocity_class": c.L4,
            },
            c.L6: {
                "code": c.L6,
                "name": "Six Lane (Two Way)",
                "width": 10.50,
                "capacity": 8400,
                "velocity_class": c.L6,
            },
            c.L8: {
                "code": c.L8,
                "name": "Eight Lane (Two Way)",
                "width": 14.00,
                "capacity": 13600,
                "velocity_class": c.L8,
            },
            # --- Expressways (Custom Width Required) ---
            c.EW4: {
                "code": c.EW4,
                "name": "4 Lane (Two Way) Expressway",
                "width": None,
                "capacity": 5000,
                "velocity_class": c.EW,
            },
            c.EW6: {
                "code": c.EW6,
                "name": "6 Lane (Two Way) Expressway",
                "width": None,
                "capacity": 7500,
                "velocity_class": c.EW,
            },
            c.EW8: {
                "code": c.EW8,
                "name": "8 Lane (Two Way) Expressway",
                "width": None,
                "capacity": 9200,
                "velocity_class": c.EW,
            },
        }
    )

    NOTE: str = (
        "Note: 'Expressway (custom width required)' requires user input. "
        "Carriageway width represents the total width of the roadway for vehicular traffic."
    )

    @classmethod
    def list_types(cls) -> Tuple[List[str], str]:
        """
        Returns:
            tuple: (list of carriageway type codes, usage note)
        """
        return list(cls._DATA.keys()), cls.NOTE

    @classmethod
    def get_width(
        cls, type_name: str, custom_width: Optional[Union[int, float]] = None
    ) -> Tuple[Optional[float], str]:
        """
        Retrieve the width for a given carriageway type.
        """

        # Validate type_name
        if not isinstance(type_name, str):
            return (
                None,
                f"Error: 'type_name' must be a string, got {type(type_name).__name__}.",
            )

        if type_name not in cls._DATA:
            return None, f"Error: Unknown carriageway type '{type_name}'."

        width = cls._DATA[type_name]["width"]

        # Standard width
        if width is not None:
            return width, "Standard width applied."  # type: ignore

        # Custom width required
        if custom_width is None:
            return None, (
                "Custom width required for this type. "
                "Please provide a width in meters (float or int). "
                "Carriageway width represents the total width of the roadway for vehicular traffic."
            )

        if not isinstance(custom_width, (int, float)):
            return None, (
                f"Error: 'custom_width' must be a number (int or float), "
                f"got {type(custom_width).__name__}."
            )

        if custom_width <= 0:
            return None, "Error: 'custom_width' must be a positive number."

        return float(custom_width), "Custom expressway width applied."

    @classmethod
    def get_capacity(cls, type_name: str) -> int:
        """
        Retrieve the capacity for a given carriageway type.

        Args:
            type_name (str): Carriageway type code.

        Returns:
            int: Capacity of the carriageway type.
        """
        return cls._DATA[type_name]["capacity"] # type: ignore

    @classmethod
    def get_suggestion(cls) -> List[dict]:
        """
        Returns full information for all carriageway types.

        Returns:
            List[dict]: Each dict contains:
                - code
                - name
                - width (or 'custom_required' if None)
                - capacity
                - velocity_class
        """
        result = []

        for item in cls._DATA.values():
            result.append(
                {
                    "code": item["code"],
                    "name": item["name"],
                    "width": item["width"] if item["width"] is not None else "custom_required",
                    "capacity": item.get("capacity", None),
                    "velocity_class": item.get("velocity_class", None),
                }
            )

        return result

    @classmethod
    def get_velocity_class(cls, type_name: str) -> str:
        """
        Retrieve the velocity class for a given carriageway type.
        Assumes 'type_name' is already validated.

        Args:
            type_name (str): Carriageway type code (e.g., 'SL', 'L2', 'EW4')

        Returns:
            str: The velocity_class for the carriageway type
        """

        return cls._DATA[type_name]["velocity_class"]  # type: ignore
