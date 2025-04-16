import os
import xml.etree.ElementTree as ET

def load_arxml_file(file_path):
    """Reads and parses an ARXML file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"⚠️ Error: File '{file_path}' not found!")
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        raise ValueError(f"⚠️ Error parsing ARXML file: {str(e)}")

def extract_element_values(root, tag_name):
    """Extracts values of all elements with a specific tag."""
    return [elem.text for elem in root.findall(f".//{tag_name}") if elem.text]

def validate_required_elements(root, required_tags):
    """Checks if required tags are present in the ARXML file."""
    missing_tags = [tag for tag in required_tags if not root.findall(f".//{tag}")]
    return missing_tags

def save_arxml_file(root, output_path):
    """Saves the modified ARXML file."""
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
