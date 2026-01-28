# CarriagewayStandards

`CarriagewayStandards` is a Python module that provides **standard carriageway widths** for different road types. It allows you to **list available road types**, retrieve **standard widths**, and **specify custom widths** for expressways.

---

## Installation

If this module is part of your project, simply ensure it is in your Python path:

```python
from mod.carriagewayStandards import CarriagewayStandards
```

No external dependencies are required (uses only standard library modules).

---

## Features

* List all available carriageway types along with a usage note.
* Retrieve the standard width for a given road type.
* Provide a custom width for expressways when the standard width is not defined.
* Includes **input validation** and helpful error messages.

---

## Usage

### List Available Carriageway Types

```python
types, note = CarriagewayStandards.list_types()
print("Available Carriageway Types:")
for t in types:
    print("-", t)
print("\nNote:", note)
```

**Output Example:**

```
Available Carriageway Types:
- Single Lane Road
- Intermediate Lane Road
- Two Lane Road
- Four-Lane (divided) Road per direction
- Six-Lane (divided) Road per direction
- Eight-Lane (divided) Road / Expressway per direction
- Expressway (custom width required)

Note: 'Expressway (custom width required)' requires user input. Carriageway width represents the total width of the roadway for vehicular traffic.
```

---

### Retrieve Standard Width

```python
width, message = CarriagewayStandards.get_width("Two Lane Road")
print(f"Width: {width} m, Message: {message}")
```

**Output Example:**

```
Width: 7.0 m, Message: Standard width applied.
```

---

### Provide Custom Width for Expressway

```python
width, message = CarriagewayStandards.get_width("Expressway (custom width required)", custom_width=14.0)
print(f"Width: {width} m, Message: {message}")
```

**Output Example:**

```
Width: 14.0 m, Message: Custom expressway width applied.
```

---

### Error Handling

* If an unknown type is provided:

```python
width, message = CarriagewayStandards.get_width("Unknown Road")
print(message)
```

Output:

```
Error: Unknown carriageway type 'Unknown Road'.
```

* If `custom_width` is invalid:

```python
width, message = CarriagewayStandards.get_width("Expressway (custom width required)", custom_width=-5)
print(message)
```

Output:

```
Error: 'custom_width' must be a positive number.
```

---

## API

### `CarriagewayStandards.list_types()`

* Returns a tuple: `(list of road types, usage note)`

### `CarriagewayStandards.get_width(type_name, custom_width=None)`

* `type_name` (str): Name of the carriageway type
* `custom_width` (float, optional): Required for expressways

Returns: `(width in meters or None, message string)`

---