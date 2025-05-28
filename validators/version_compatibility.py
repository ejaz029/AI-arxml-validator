import xml.etree.ElementTree as ET

SUPPORTED_AUTOSAR_VERSIONS = {"4.2.2", "4.3.1", "4.4.0"}

def extract_autosar_version(root):
    """
    Extracts the AUTOSAR version from xsi:schemaLocation.
    """
    schema_location = root.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", "")
    for token in schema_location.split():
        if "AUTOSAR_" in token:
            return token.split("AUTOSAR_")[-1].replace(".xsd", "")
    return None

def check_autosar_version(root):
    errors = []
    version = extract_autosar_version(root)

    if version:
        if version not in SUPPORTED_AUTOSAR_VERSIONS:
            errors.append(f"⚠️ Unsupported AUTOSAR version detected: {version}")
    else:
        errors.append("⚠️ AUTOSAR version could not be determined from schemaLocation.")
    
    return errors

def check_deprecated_elements(root):
    errors = []
    deprecated_elements = ["OLD-SIGNAL-MAPPING", "OBSOLETE-COM-INTERFACE"]

    for deprecated in deprecated_elements:
        if root.findall(f".//{deprecated}"):
            errors.append(f"⚠️ Deprecated AUTOSAR element found: {deprecated}")

    return errors

def validate_autosar_version(root):
    errors = []
    errors.extend(check_autosar_version(root))
    errors.extend(check_deprecated_elements(root))
    return errors

# Example usage
if __name__ == "__main__":
    file_path = "example.arxml"
    tree = ET.parse(file_path)
    root = tree.getroot()

    errors = validate_autosar_version(root)

    if errors:
        print("❌ AUTOSAR Version Compatibility Errors:")
        for error in errors:
            print(error)
    else:
        print("✅ AUTOSAR Version Compatibility Validation Passed!")

