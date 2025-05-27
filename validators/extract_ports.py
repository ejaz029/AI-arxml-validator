# extract_ports.py
import xml.etree.ElementTree as ET
import os

def extract_ports_from_arxml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract namespace if present
        ns = {'ns': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}

        ports = []

        for p_port in root.findall(".//ns:P-PORT-PROTOTYPE", ns):
            name = p_port.findtext("ns:SHORT-NAME", default="N/A", namespaces=ns)
            interface = p_port.findtext(".//ns:PROVIDED-INTERFACE-TREF", default="N/A", namespaces=ns)
            ports.append({
                "port_type": "P-PORT",
                "name": name,
                "interface": interface
            })

        for r_port in root.findall(".//ns:R-PORT-PROTOTYPE", ns):
            name = r_port.findtext("ns:SHORT-NAME", default="N/A", namespaces=ns)
            interface = r_port.findtext(".//ns:REQUIRED-INTERFACE-TREF", default="N/A", namespaces=ns)
            ports.append({
                "port_type": "R-PORT",
                "name": name,
                "interface": interface
            })

        return ports
    except Exception as e:
        return [{"error": f"Failed to parse {file_path}: {e}"}]
