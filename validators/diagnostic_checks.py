import xml.etree.ElementTree as ET

def validate_dtc_uniqueness(root):
    """
    Ensures all Diagnostic Trouble Codes (DTCs) are unique.
    """
    dtc_set = set()
    errors = []

    for dtc in root.findall(".//DEM-EVENT/DTC"):
        dtc_value = dtc.text.strip() if dtc.text else None
        if dtc_value:
            if dtc_value in dtc_set:
                errors.append(f"⚠️ Duplicate DTC found: {dtc_value}")
            else:
                dtc_set.add(dtc_value)

    return errors

def validate_dem_event_mappings(root):
    """
    Ensures each Diagnostic Event (DEM) is mapped to a valid reporting method.
    """
    valid_methods = {"ONDEMAND", "CYCLIC", "TIME-BASED", "CONDITIONAL"}
    errors = []

    for event in root.findall(".//DEM-EVENT"):
        event_name = event.find("SHORT-NAME").text if event.find("SHORT-NAME") is not None else "Unknown"
        method_elem = event.find("REPORTING-METHOD")
        
        if method_elem is None or method_elem.text not in valid_methods:
            errors.append(f"⚠️ Invalid or missing reporting method for DEM Event: {event_name}")

    return errors

def validate_dem_event_references(root):
    """
    Ensures all referenced diagnostic events exist in the ARXML file.
    """
    defined_events = set()
    referenced_events = set()
    errors = []

    for event in root.findall(".//DEM-EVENT"):
        event_name = event.find("SHORT-NAME").text if event.find("SHORT-NAME") is not None else None
        if event_name:
            defined_events.add(event_name)

    for ref in root.findall(".//DEM-EVENT-REF"):
        ref_name = ref.text.strip() if ref.text else None
        if ref_name:
            referenced_events.add(ref_name)

    for ref in referenced_events:
        if ref not in defined_events:
            errors.append(f"⚠️ Undefined DEM Event Reference: {ref}")

    return errors

# Example Usage
if __name__ == "__main__":
    file_path = "example.arxml"
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    errors = []
    errors.extend(validate_dtc_uniqueness(root))
    errors.extend(validate_dem_event_mappings(root))
    errors.extend(validate_dem_event_references(root))

    if errors:
        print("❌ DEM/DTC Validation Errors:")
        for error in errors:
            print(error)
    else:
        print("✅ DEM/DTC Validation Passed!")
