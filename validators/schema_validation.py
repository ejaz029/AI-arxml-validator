# import os
# from lxml import etree

# def validate_arxml_schema(arxml_file, xsd_file):
#     """
#     Validates an ARXML file against an AUTOSAR XSD schema.
    
#     :param arxml_file: Path to the ARXML file.
#     :param xsd_file: Path to the AUTOSAR XSD schema file.
#     :return: Tuple (is_valid, error_messages)
#     """
#     # Check file existence with absolute paths
#     if not os.path.exists(arxml_file):
#         raise FileNotFoundError(f"⚠️ Error: ARXML file '{os.path.abspath(arxml_file)}' not found!")

#     if not os.path.exists(xsd_file):
#         raise FileNotFoundError(f"⚠️ Error: XSD schema file '{os.path.abspath(xsd_file)}' not found!")

#     try:
#         # Load the XML Schema efficiently
#         schema_doc = etree.parse(xsd_file)
#         schema = etree.XMLSchema(schema_doc)

#         # Parse the ARXML file with explicit encoding
#         with open(arxml_file, "rb") as arxml:
#             parser = etree.XMLParser(encoding="utf-8")
#             arxml_doc = etree.parse(arxml, parser)
        
#         # Validate ARXML against XSD
#         is_valid = schema.validate(arxml_doc)
#         if not is_valid:
#             errors = schema.error_log
#             error_messages = [f"❌ Line {error.line}: {error.message}" for error in errors]
#             return False, error_messages
        
#         return True, None

#     except etree.XMLSyntaxError as e:
#         return False, [f"⚠️ XML Syntax Error: {str(e)}"]

#     except Exception as e:
#         return False, [f"⚠️ Unexpected Error: {str(e)}"]

# # Example Usage
# if __name__ == "__main__":
#     arxml_path = "example.arxml"
#     xsd_path = "AUTOSAR_schema.xsd"
    
#     valid, errors = validate_arxml_schema(arxml_path, xsd_path)
#     if valid:
#         print("✅ ARXML file is schema-valid!")
#     else:
#         print("❌ Schema validation failed:", errors)
import os
from lxml import etree
import requests
import tempfile

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
        # Create a temporary file for xml.xsd if it doesn't exist
        xml_xsd_path = os.path.join(os.path.dirname(xsd_file), "xml.xsd")
        
        # If xml.xsd doesn't exist in the same folder as the schema, create it
        if not os.path.exists(xml_xsd_path):
            # Standard XML namespace schema content
            xml_xsd_content = """<?xml version='1.0'?>
<xs:schema targetNamespace="http://www.w3.org/XML/1998/namespace" 
           xmlns:xs="http://www.w3.org/2001/XMLSchema" 
           xml:lang="en">

 <xs:attribute name="lang" type="xs:language">
  <xs:annotation>
   <xs:documentation>Specifies the language used in the element content.</xs:documentation>
  </xs:annotation>
 </xs:attribute>

 <xs:attribute name="space">
  <xs:annotation>
   <xs:documentation>Specifies significant whitespace treatment.</xs:documentation>
  </xs:annotation>
  <xs:simpleType>
   <xs:restriction base="xs:NCName">
    <xs:enumeration value="default"/>
    <xs:enumeration value="preserve"/>
   </xs:restriction>
  </xs:simpleType>
 </xs:attribute>

 <xs:attribute name="base" type="xs:anyURI">
  <xs:annotation>
   <xs:documentation>Base URI to resolve relative URIs.</xs:documentation>
  </xs:annotation>
 </xs:attribute>

 <xs:attribute name="id" type="xs:ID">
  <xs:annotation>
   <xs:documentation>Document identifier.</xs:documentation>
  </xs:annotation>
 </xs:attribute>

 <xs:attributeGroup name="specialAttrs">
  <xs:attribute ref="xml:base"/>
  <xs:attribute ref="xml:lang"/>
  <xs:attribute ref="xml:space"/>
  <xs:attribute ref="xml:id"/>
 </xs:attributeGroup>

</xs:schema>"""
            
            # Write the XML schema to a temporary file
            with open(xml_xsd_path, 'w', encoding='utf-8') as f:
                f.write(xml_xsd_content)
            
            # Set flag to clean up the temporary file later
            cleanup_needed = True
        else:
            cleanup_needed = False
            
        try:
            # Parse and validate with the schema
            parser = etree.XMLParser(resolve_entities=True, recover=True)
            arxml_doc = etree.parse(arxml_file, parser)
            
            schema_doc = etree.parse(xsd_file, parser)
            schema = etree.XMLSchema(schema_doc)
            
            # Validate ARXML against XSD
            is_valid = schema.validate(arxml_doc)
            if not is_valid:
                errors = schema.error_log
                error_messages = [f"❌ Line {error.line}: {error.message}" for error in errors]
                return False, error_messages
                
            return True, None
            
        finally:
            # Clean up the temporary xml.xsd file if we created it
            if cleanup_needed and os.path.exists(xml_xsd_path):
                try:
                    os.remove(xml_xsd_path)
                except:
                    pass
    
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