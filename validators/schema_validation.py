import os
from lxml import etree

def validate_arxml_schema(arxml_file, xsd_file):
    """
    Validates an ARXML file against an AUTOSAR XSD schema.
    
    :param arxml_file: Path to the ARXML file.
    :param xsd_file: Path to the AUTOSAR XSD schema file.
    :return: Tuple (is_valid, error_messages)
    """
    # Check file existence with absolute paths
    if not os.path.exists(arxml_file):
        raise FileNotFoundError(f"⚠️ Error: ARXML file '{os.path.abspath(arxml_file)}' not found!")

    if not os.path.exists(xsd_file):
        raise FileNotFoundError(f"⚠️ Error: XSD schema file '{os.path.abspath(xsd_file)}' not found!")

    try:
        # Load the XML Schema efficiently
        schema_doc = etree.parse(xsd_file)
        schema = etree.XMLSchema(schema_doc)

        # Parse the ARXML file with explicit encoding
        with open(arxml_file, "rb") as arxml:
            parser = etree.XMLParser(encoding="utf-8")
            arxml_doc = etree.parse(arxml, parser)
        
        # Validate ARXML against XSD
        is_valid = schema.validate(arxml_doc)
        if not is_valid:
            errors = schema.error_log
            error_messages = [f"❌ Line {error.line}: {error.message}" for error in errors]
            return False, error_messages
        
        return True, None

    except etree.XMLSyntaxError as e:
        return False, [f"⚠️ XML Syntax Error: {str(e)}"]

    except Exception as e:
        return False, [f"⚠️ Unexpected Error: {str(e)}"]

# Example Usage
if __name__ == "__main__":
    arxml_path = "example.arxml"
    xsd_path = "AUTOSAR_schema.xsd"
    
    valid, errors = validate_arxml_schema(arxml_path, xsd_path)
    if valid:
        print("✅ ARXML file is schema-valid!")
    else:
        print("❌ Schema validation failed:", errors)
