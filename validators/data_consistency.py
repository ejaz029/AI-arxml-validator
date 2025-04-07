import xml.etree.ElementTree as ET

def validate_uuid_uniqueness(root):
    """Ensures all UUIDs are unique within the ARXML file."""
    uuids = {}
    errors = []

    for elem in root.findall(".//*[@UUID]"):  # Find all elements with UUID
        uuid = elem.attrib.get("UUID")
        if uuid:
            if uuid in uuids:
                errors.append(f"⚠️ Duplicate UUID found: {uuid}")
            else:
                uuids[uuid] = elem.tag

    return errors

def validate_required_attributes(root, required_attributes):
    """Ensures all required attributes are present in the ARXML file."""
    errors = []

    for elem in root.iter():
        for attr in required_attributes:
            if attr not in elem.attrib:
                element_name = elem.tag
                errors.append(f"⚠️ Missing required attribute '{attr}' in element <{element_name}>")

    return errors

def validate_referenced_elements(root):
    """Ensures all references in the ARXML file point to valid existing elements."""
    existing_ids = set()
    errors = []

    # Collect all existing IDs
    for elem in root.iter():
        if "ID" in elem.attrib:
            existing_ids.add(elem.attrib["ID"])

    # Validate references
    for elem in root.findall(".//*[@REFERENCE]"):  # Find elements with REFERENCE attributes
        reference = elem.attrib.get("REFERENCE")
        if reference and reference not in existing_ids:
            errors.append(f"⚠️ Broken reference: {reference} not found in the ARXML file.")

    return errors

# ✅ Fix: Define validate_data function
def validate_data(root):
    """Runs all validation checks on the ARXML file."""
    required_attributes = ["UUID", "ID"]
    errors = []
    errors.extend(validate_uuid_uniqueness(root))
    errors.extend(validate_required_attributes(root, required_attributes))
    errors.extend(validate_referenced_elements(root))

    return errors
