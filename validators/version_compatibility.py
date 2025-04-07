import xml.etree.ElementTree as ET

# Define supported AUTOSAR versions
SUPPORTED_AUTOSAR_VERSIONS = {"4.2.2", "4.3.1", "4.4.0"}

def check_autosar_version(root):
    """
    Checks if the AUTOSAR version used in the file is consistent across all components
    and is within the supported versions.
    """
    errors = []
    version_set = set()

    for element in root.findall(".//AUTOSAR"):
        version = element.get("AR-PACKAGE-VERSION", None)

        if version:
            version_set.add(version)
            if version not in SUPPORTED_AUTOSAR_VERSIONS:
                errors.append(f"⚠️ Unsupported AUTOSAR version detected: {version}")

    if len(version_set) > 1:
        errors.append(f"⚠️ Inconsistent AUTOSAR versions found: {', '.join(version_set)}")
    
    return errors

def check_deprecated_elements(root):
    """
    Checks if any deprecated AUTOSAR elements are present in the ARXML file.
    """
    errors = []
    deprecated_elements = ["OLD-SIGNAL-MAPPING", "OBSOLETE-COM-INTERFACE"]

    for deprecated in deprecated_elements:
        if root.findall(f".//{deprecated}"):
            errors.append(f"⚠️ Deprecated AUTOSAR element found: {deprecated}")

    return errors

def validate_autosar_version(root):
    """
    Runs all AUTOSAR version validation checks.
    """
    errors = []
    errors.extend(check_autosar_version(root))
    errors.extend(check_deprecated_elements(root))

    return errors

# Example Usage
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
