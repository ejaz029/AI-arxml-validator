import xml.etree.ElementTree as ET
import os

def extract_ports_from_arxml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        ns = {'ns': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}

        ports = set()

        for p_port in root.findall(".//ns:P-PORT-PROTOTYPE", ns):
            name = p_port.findtext("ns:SHORT-NAME", default="N/A", namespaces=ns)
            interface = p_port.find("ns:PROVIDED-INTERFACE-TREF", ns)
            interface_text = interface.text if interface is not None else "N/A"
            ports.add((
                "P-PORT",
                name,
                interface_text
            ))

        for r_port in root.findall(".//ns:R-PORT-PROTOTYPE", ns):
            name = r_port.findtext("ns:SHORT-NAME", default="N/A", namespaces=ns)
            interface = r_port.find("ns:REQUIRED-INTERFACE-TREF", ns)
            interface_text = interface.text if interface is not None else "N/A"
            ports.add((
                "R-PORT",
                name,
                interface_text
            ))

        return [{"port_type": pt, "name": name, "interface": iface} for pt, name, iface in sorted(ports)]
    except Exception as e:
        return [{"error": f"Failed to parse {file_path}: {e}"}]
