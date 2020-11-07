import unittest
from ddt import ddt, data

from src.certification import CertificationDeserializationError, Certification

@ddt
class TestCertification(unittest.TestCase):

    @data(
        # Base infos missing
        [],
        ["Luc Legardeur"],
        ["Luc Legardeur", "Oui"],
        ["Luc Legardeur", "Oui", "CKA"],
        # Certification active but with missing infos
        ["Luc Legardeur", "Oui", "CKA", "Active"],
        ["Luc Legardeur", "Oui", "CKA", "Active", "Some date"],
        ["Luc Legardeur", "Oui", "CKA", "Active", "Some date", "Some other date"]
        )
    def test_deserialize_with_missing_data_should_raise_exception(self, value):
        row = value
        # pytlint: disable=syntax-error
        with self.assertRaises(CertificationDeserializationError.MissingInfo):
            Certification(row)

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()
