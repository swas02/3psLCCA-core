## `validate_input(vehicle_input)`

Validates user-provided vehicle and carriageway parameters before further processing.
Raises a `ValueError` containing all validation errors if any rule fails.

### **Parameters**

* **vehicle_input** (`dict`):
  A dictionary containing vehicle and lane configuration fields.

### **Validation Logic**

1. **Vehicle Type (`vehicle_type`)**

   * Must be a string.
   * Must exist in `constants.vehicle_type_list`.

2. **Lane Type (`lane_type`)**

   * Must be a string.
   * Must match one of the available types returned by
     `CarriagewayStandards.list_types()`.

3. **Carriageway Width**

   * If `lane_type == "EW"` (Expressway), the user must supply a positive numeric `carriageway_width`.
   * Otherwise, a standard width is retrieved via
     `CarriagewayStandards.get_width(lane_type)` and injected into `vehicle_input`.

4. **Numeric Fields**
   The following must be numbers (`int` or `float`):

   * `rg_roughness_factor`
   * `fl_fall_factor`
   * `rf_rise_factor`

5. **Power-Weight Ratio Requirement**

   * For `vehicle_type` `"LCV"` or `"MCV"`,
     `power_weight_ratio_pwr` must be provided and numeric.

### **Behavior**

* Collects all validation errors.
* If any error exists → raises `ValueError` summarizing all issues.
* If all checks pass → returns `True`.
