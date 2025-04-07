import xml.etree.ElementTree as ET

def validate_ecu_extract_references(root):
    """
    Ensures ECU-EXTRACT correctly references ECU configurations.
    """
    ecu_refs = set()
    defined_ecus = set()
    errors = []

    # Collect defined ECUs
    for elem in root.findall(".//ECU"):
        ecu_name = elem.find("SHORT-NAME").text if elem.find("SHORT-NAME") is not None else None
        if ecu_name:
            defined_ecus.add(ecu_name)

    # Collect ECU references in ECU-EXTRACT
    for elem in root.findall(".//ECU-EXTRACT/ECU-REF"):
        ref = elem.text
        if ref:
            ecu_refs.add(ref)

    # Validate ECU references
    for ref in ecu_refs:
        if ref not in defined_ecus:
            errors.append(f"⚠️ Undefined ECU reference found in ECU-EXTRACT: {ref}")

    return errors

def validate_bsw_module_configurations(root):
    """
    Ensures consistency between BSW modules (COM, DEM, DIO, CAN, LIN) and software components.
    """
    bsw_modules = ["COM", "DEM", "DIO", "CAN", "LIN"]
    defined_modules = set()
    referenced_modules = set()
    errors = []

    # Collect defined BSW modules
    for elem in root.findall(".//BSW-MODULE"):
        module_name = elem.find("SHORT-NAME").text if elem.find("SHORT-NAME") is not None else None
        if module_name:
            defined_modules.add(module_name)

    # Collect referenced BSW modules
    for elem in root.findall(".//BSW-CONFIG/BSW-MODULE-REF"):
        ref = elem.text
        if ref:
            referenced_modules.add(ref)

    # Validate references
    for ref in referenced_modules:
        if ref not in defined_modules:
            errors.append(f"⚠️ Undefined BSW module reference found: {ref}")

    # Check if required BSW modules are missing
    for module in bsw_modules:
        if module not in defined_modules:
            errors.append(f"⚠️ Missing required BSW module: {module}")

    return errors

def validate_ecu_bsw_alignment(root):
    """
    Ensures ECU and BSW configurations are correctly aligned.
    """
    ecu_config = set()
    bsw_config = set()
    errors = []

    # Collect ECU configuration items
    for elem in root.findall(".//ECU-CONFIGURATION"):
        item = elem.find("SHORT-NAME").text if elem.find("SHORT-NAME") is not None else None
        if item:
            ecu_config.add(item)

    # Collect BSW configuration items
    for elem in root.findall(".//BSW-CONFIGURATION"):
        item = elem.find("SHORT-NAME").text if elem.find("SHORT-NAME") is not None else None
        if item:
            bsw_config.add(item)

    # Validate alignment
    for config in ecu_config:
        if config not in bsw_config:
            errors.append(f"⚠️ ECU Configuration '{config}' does not match any BSW Configuration.")

    return errors

# Example Usage
if __name__ == "__main__":
    file_path = "example.arxml"
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    errors = []
    errors.extend(validate_ecu_extract_references(root))
    errors.extend(validate_bsw_module_configurations(root))
    errors.extend(validate_ecu_bsw_alignment(root))

    if errors:
        print("❌ ECU & BSW Configuration Validation Errors:")
        for error in errors:
            print(error)
    else:
        print("✅ ECU & BSW Configuration Validation Passed!")
