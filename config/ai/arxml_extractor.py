import xml.etree.ElementTree as ET

def extract_arxml_data(file_path):
    """
    Extracts relevant data from an ARXML file for AI-based validation.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        extracted_data = {
            "swc_components": [],
            "ports": [],
            "pdus": [],
            "signals": [],
            "diagnostics": []
        }

        # Extract Software Components (SWC)
        for swc in root.findall(".//APPLICATION-SOFTWARE-COMPONENT-TYPE"):
            extracted_data["swc_components"].append(swc.findtext("SHORT-NAME"))

        # Extract Ports
        for port in root.findall(".//PORT"):
            extracted_data["ports"].append({
                "name": port.findtext("SHORT-NAME"),
                "interface": port.findtext("PORT-INTERFACE"),
                "data_type": port.findtext("DATA-TYPE")
            })

        # Extract PDUs
        for pdu in root.findall(".//PDU"):
            extracted_data["pdus"].append(pdu.findtext("SHORT-NAME"))

        # Extract Signals
        for signal in root.findall(".//SIGNAL"):
            extracted_data["signals"].append({
                "name": signal.findtext("SHORT-NAME"),
                "sender": signal.findtext("SENDER"),
                "receiver": signal.findtext("RECEIVER")
            })

        # Extract Diagnostics (DEM/DTC)
        for diag in root.findall(".//DEM-EVENT"):
            extracted_data["diagnostics"].append({
                "event_name": diag.findtext("SHORT-NAME"),
                "dtc": diag.findtext("DTC-VALUE")
            })

        return extracted_data
    
    except ET.ParseError:
        return {"error": "Invalid XML format. Unable to parse ARXML file."}
    except Exception as e:
        return {"error": str(e)}

# Example Usage
if __name__ == "__main__":
    file_path = "example.arxml"
    extracted_info = extract_arxml_data(file_path)
    print(extracted_info)
