import unittest
from ai.rag_validation import validate_arxml_with_rag
from ai.ai_chatbot import chat_with_ai

class TestAI(unittest.TestCase):
    def setUp(self):
        self.sample_arxml_path = "test_data/sample.arxml"
        self.test_query = "Check the ARXML file for inconsistencies."

    def test_rag_validation(self):
        """Test AI-powered validation on ARXML file."""
        response = validate_arxml_with_rag(self.sample_arxml_path)
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, "")

    def test_ai_chatbot(self):
        """Test AI chatbot interaction."""
        response = chat_with_ai(self.test_query, self.sample_arxml_path)
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, "")

if __name__ == "__main__":
    unittest.main()
