import xml.etree.ElementTree as ET

def validate_pdu_definitions(root):
    """
    Ensures all PDU (Protocol Data Units) definitions are correctly referenced.
    """
    pdu_refs = set()
    defined_pdus = set()
    errors = []

    # Collect defined PDUs
    for elem in root.findall(".//PDU"):
        pdu_name = elem.find("SHORT-NAME").text if elem.find("SHORT-NAME") is not None else None
        if pdu_name:
            defined_pdus.add(pdu_name)

    # Collect referenced PDUs
    for elem in root.findall(".//PDU-REF"):
        ref = elem.text
        if ref:
            pdu_refs.add(ref)

    # Validate references
    for ref in pdu_refs:
        if ref not in defined_pdus:
            errors.append(f"⚠️ Undefined PDU reference found: {ref}")

    return errors

def validate_signal_to_pdu_mapping(root):
    """
    Ensures all signals are correctly mapped to a valid PDU.
    """
    signal_pdu_mapping = {}
    errors = []

    # Find all signals and their associated PDU
    for elem in root.findall(".//SIGNAL-TO-PDU-MAPPING"):
        signal = elem.find("SIGNAL-REF")
        pdu = elem.find("PDU-REF")

        if signal is not None and pdu is not None:
            signal_name = signal.text
            pdu_name = pdu.text
            signal_pdu_mapping[signal_name] = pdu_name

    # Validate the mappings
    for signal, pdu in signal_pdu_mapping.items():
        if not pdu:
            errors.append(f"⚠️ Signal '{signal}' is not assigned to any valid PDU!")

    return errors

def validate_com_module(root):
    """
    Ensures there are no undefined signals in the COM module.
    """
    defined_signals = set()
    referenced_signals = set()
    errors = []

    # Collect defined signals
    for elem in root.findall(".//SIGNAL"):
        signal_name = elem.find("SHORT-NAME").text if elem.find("SHORT-NAME") is not None else None
        if signal_name:
            defined_signals.add(signal_name)

    # Collect referenced signals
    for elem in root.findall(".//SIGNAL-REF"):
        if elem.text:
            referenced_signals.add(elem.text)

    # Validate referenced signals exist
    for ref_signal in referenced_signals:
        if ref_signal not in defined_signals:
            errors.append(f"⚠️ Undefined signal reference found in COM module: {ref_signal}")

    return errors

# Example Usage
if __name__ == "__main__":
    file_path = "example.arxml"
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    errors = []
    errors.extend(validate_pdu_definitions(root))
    errors.extend(validate_signal_to_pdu_mapping(root))
    errors.extend(validate_com_module(root))

    if errors:
        print("❌ Communication & PDU Validation Errors:")
        for error in errors:
            print(error)
    else:
        print("✅ Communication & PDU Validation Passed!")
