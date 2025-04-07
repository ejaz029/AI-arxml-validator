import xml.etree.ElementTree as ET

def validate_rte_event_mappings(root):
    """
    Ensures each RTE event is mapped to a valid runnable entity.
    """
    errors = []

    for event in root.findall(".//RTE-EVENT"):
        event_name = event.find("SHORT-NAME").text if event.find("SHORT-NAME") is not None else "Unknown"
        runnable_ref = event.find("RUNNABLE-REF")

        if runnable_ref is None or not runnable_ref.text:
            errors.append(f"⚠️ Missing runnable mapping for RTE Event: {event_name}")

    return errors

def validate_synchronization_points(root):
    """
    Ensures synchronization points are correctly defined in the RTE.
    """
    errors = []

    for sync_point in root.findall(".//SYNCHRONIZATION-POINT"):
        sync_name = sync_point.find("SHORT-NAME").text if sync_point.find("SHORT-NAME") is not None else "Unknown"
        sync_type = sync_point.find("TYPE").text if sync_point.find("TYPE") is not None else None

        if not sync_type or sync_type not in {"BARRIER", "MUTEX"}:
            errors.append(f"⚠️ Invalid synchronization type for {sync_name}: {sync_type}")

    return errors

def validate_port_interface_consistency(root):
    """
    Ensures all ports are correctly mapped to their interfaces.
    """
    port_interfaces = set()
    errors = []

    for interface in root.findall(".//PORT-INTERFACE"):
        interface_name = interface.find("SHORT-NAME").text if interface.find("SHORT-NAME") is not None else None
        if interface_name:
            port_interfaces.add(interface_name)

    for port in root.findall(".//PORT"):
        interface_ref = port.find("PORT-INTERFACE-REF")
        port_name = port.find("SHORT-NAME").text if port.find("SHORT-NAME") is not None else "Unknown"

        if interface_ref is None or interface_ref.text not in port_interfaces:
            errors.append(f"⚠️ Invalid or missing PORT-INTERFACE reference for port: {port_name}")

    return errors

# Example Usage
if __name__ == "__main__":
    file_path = "example.arxml"
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    errors = []
    errors.extend(validate_rte_event_mappings(root))
    errors.extend(validate_synchronization_points(root))
    errors.extend(validate_port_interface_consistency(root))

    if errors:
        print("❌ RTE Validation Errors:")
        for error in errors:
            print(error)
    else:
        print("✅ RTE Configuration Validation Passed!")
