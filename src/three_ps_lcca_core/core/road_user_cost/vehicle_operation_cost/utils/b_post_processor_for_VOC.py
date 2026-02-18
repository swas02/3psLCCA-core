from typing import Any, Dict
from .c_wpi_adjustment import VOCPostProcessor, calculate_total_cost
from ....utils.dump_to_file import dump_to_file

def post_process(outputFromVocOutputBuilder: Dict[str, Any], wpi: Dict[str, Any], debug: bool = False) -> Dict[str, Any]:
    """Orchestrates the WPI adjustment and handles debugging dumps."""
    
    # 1. Initialize the engine from the new file
    processor = VOCPostProcessor(wpi)
    
    # 2. Run the adjustment
    wpiAdjustedValues = processor.process(outputFromVocOutputBuilder)
    
    # 3. Aggregate for the final summary
    summaryOfVOC = calculate_total_cost(wpiAdjustedValues)

    if debug:
        dump_to_file("ruc-voc-1-Base.json", outputFromVocOutputBuilder)
        dump_to_file("ruc-voc-2-WPI-Adjusted.json", wpiAdjustedValues)
        dump_to_file("ruc-voc-3-Final-Summary.json", summaryOfVOC)

    return summaryOfVOC