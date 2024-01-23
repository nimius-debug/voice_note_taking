import unittest
from summarize import summarize_text

class TestUtils(unittest.TestCase):
    def test_summarize_text(self):
        # Assuming summarize_text returns a tuple (summary, length)
        text = "This is a test text."
        summary, length = summarize_text(text, 0)
        self.assertTrue(len(summary) > 0)
        self.assertEqual(length, len(text))

if __name__ == '__main__':
    unittest.main()
