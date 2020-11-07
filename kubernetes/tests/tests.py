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
    def test_missing_data_should_raise_exception(self, value):
        with self.assertRaises(CertificationDeserializationError.MissingInfo):
            Certification(value)

    def test_invalid_employment_status_should_raise_exception(self):
        row = ["Luc Legardeur", "Maybe?", "CKA", "En cours de préparation"]
        with self.assertRaises(CertificationDeserializationError.InvalidValue):
            Certification(row)

    def test_invalid_certification_status_should_raise_exception(self):
        row = ["Luc Legardeur", "Oui", "CKA", "Some INEXISTING status"]
        with self.assertRaises(CertificationDeserializationError.InvalidValue):
            Certification(row)

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()
