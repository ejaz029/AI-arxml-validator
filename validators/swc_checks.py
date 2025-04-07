import xml.etree.ElementTree as ET

def check_swc_definitions(root):
    """
    Ensures that each <APPLICATION-SOFTWARE-COMPONENT-TYPE> has correctly defined ports and interfaces.
    """
    errors = []
    for swc in root.findall(".//APPLICATION-SOFTWARE-COMPONENT-TYPE"):
        swc_name = swc.findtext("SHORT-NAME")
        ports = swc.findall(".//PORT")
        if not ports:
            errors.append(f"⚠️ SWC {swc_name} has no defined ports.")
    return errors

def check_runnable_entities(root):
    """
    Ensures that all runnable entities have correctly defined triggers (DATA-RECEIVED-EVENT, TIMING-EVENT, etc.).
    """
    errors = []
    for runnable in root.findall(".//RUNNABLE-ENTITY"):
        runnable_name = runnable.findtext("SHORT-NAME")
        triggers = runnable.findall(".//DATA-RECEIVED-EVENT") + runnable.findall(".//TIMING-EVENT")
        if not triggers:
            errors.append(f"⚠️ Runnable {runnable_name} has no defined triggers.")
    return errors

def check_port_data_types(root):
    """
    Ensures that producer (P-PORT) and receiver (R-PORT) ports match in data type and interface.
    """
    errors = []
    port_data_types = {}

    for port in root.findall(".//PORT"):
        port_name = port.findtext("SHORT-NAME")
        data_type = port.findtext("DATA-TYPE")
        port_interface = port.findtext("PORT-INTERFACE")

        if port_name and data_type and port_interface:
            port_data_types[port_name] = (data_type, port_interface)

    for p_port, (p_data_type, p_interface) in port_data_types.items():
        for r_port, (r_data_type, r_interface) in port_data_types.items():
            if p_interface == r_interface and p_data_type != r_data_type:
                errors.append(f"⚠️ Data type mismatch between {p_port} (P-PORT) and {r_port} (R-PORT).")
    return errors

def validate_swc_checks(root):
    """
    Runs all software component validation checks.
    """
    errors = []
    errors.extend(check_swc_definitions(root))
    errors.extend(check_runnable_entities(root))
    errors.extend(check_port_data_types(root))
    return errors

# Example Usage
if __name__ == "__main__":
    file_path = "example.arxml"
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    errors = validate_swc_checks(root)

    if errors:
        print("❌ Software Component Validation Errors:")
        for error in errors:
            print(error)
    else:
        print("✅ Software Component Validation Passed!")
