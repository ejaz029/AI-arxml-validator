import unittest
import xml.etree.ElementTree as ET
from validators.schema_validator import validate_arxml_schema
from validators.data_consistency import check_uuid_uniqueness, check_required_attributes
from validators.communication_checks import validate_pdu_mapping
from validators.rte_checks import validate_rte_configuration

class TestARXMLValidations(unittest.TestCase):
    def setUp(self):
        """Load an example ARXML file for testing."""
        self.arxml_content = """
        <AUTOSAR>
            <AR-PACKAGES>
                <AR-PACKAGE>
                    <SHORT-NAME>TestPackage</SHORT-NAME>
                    <ELEMENTS>
                        <UUID>123e4567-e89b-12d3-a456-426614174000</UUID>
                    </ELEMENTS>
                </AR-PACKAGE>
            </AR-PACKAGES>
        </AUTOSAR>
        """
        self.root = ET.ElementTree(ET.fromstring(self.arxml_content)).getroot()

    def test_schema_validation(self):
        """Test if ARXML schema validation works correctly."""
        errors = validate_arxml_schema("test_file.arxml")
        self.assertIsInstance(errors, list)

    def test_uuid_uniqueness(self):
        """Test UUID uniqueness check."""
        errors = check_uuid_uniqueness(self.root)
        self.assertEqual(errors, [])  # Expect no errors for unique UUID

    def test_required_attributes(self):
        """Test required attributes validation."""
        errors = check_required_attributes(self.root)
        self.assertIsInstance(errors, list)

    def test_pdu_mapping(self):
        """Test PDU mapping validation."""
        errors = validate_pdu_mapping(self.root)
        self.assertIsInstance(errors, list)

    def test_rte_configuration(self):
        """Test RTE configuration validation."""
        errors = validate_rte_configuration(self.root)
        self.assertIsInstance(errors, list)

if __name__ == "__main__":
    unittest.main()
