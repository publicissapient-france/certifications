import unittest
from ddt import ddt, data

from src.certification import CertificationDeserializationError, Certification

@ddt
class TestCertificationErrors(unittest.TestCase):

    @data(
        [],
        ["Luc Legardeur"],
        ["Luc Legardeur", "Oui"],
        ["Luc Legardeur", "Oui", "CKAD"],
        )
    def test_missing_basic_infos(self, value):
        '''
        When basic information (name, employment status, certification
        name/status) are missing, an appropriate Exception should be raised
        '''
        with self.assertRaises(CertificationDeserializationError.MissingInfo):
            Certification(value)
    
    @data(
        ["Luc", "Oui", "CKAD", "Active"],
        ["Luc", "Oui", "CKAD", "Active", "Some date"],
        ["Luc", "Oui", "CKAD", "Active", "Some date", "Some other date"]
        )
    def test_missing_infos_for_active_certification(self, value):
        '''
        When information about an Active certification (pass/expiration date,
        ID) are missing, an appropriate Exception should be raised.
        '''
        with self.assertRaises(CertificationDeserializationError.MissingInfo):
            Certification(value)

    def test_invalid_employment_status(self):
        row = ["Luc", "Maybe?", "CKAD", "En cours de préparation"]
        with self.assertRaises(CertificationDeserializationError.InvalidValue):
            Certification(row)

    def test_invalid_certification_status(self):
        row = ["Luc", "Oui", "CKAD", "Some INEXISTING status"]
        with self.assertRaises(CertificationDeserializationError.InvalidValue):
            Certification(row)

    def test_expiration_date_before_obtention_date(self):
        row = ["Luc", "Oui", "CKAD", "Active",
               "1 janvier 2023", "1 janvier 2020", "Some ID"]
        with self.assertRaises(CertificationDeserializationError.IncoherentValues):
            Certification(row)

    # def test_preparing(self):
    #     row = ["Luc Legardeur", "Oui", "CKAD", "En cours de préparation"]
    #     certification = Certification(row)
    #     self.assertEquals(certification.name, "Luc Legardeur")
    #     self.assertEquals(certification.currently_employed, "Luc Legardeur")

if __name__ == '__main__':
    unittest.main()
