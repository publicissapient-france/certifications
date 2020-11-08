import unittest
import datetime
from ddt import ddt, data

from src.certification import (
    CertificationDeserializationError,
    Certification,
    CertificationStatus,
    CertificateIdFormat,
)

# fmt: off
VALID_SAMPLE = [
    "Luc Legardeur",    # 0
    "Oui",              # 1
    "CKAD",             # 2
    "Active",           # 3
    "1 janvier 2020",   # 4
    "2 janvier 2023",   # 5
    "LF-abc123def4",    # 6
]
# fmt: on


@ddt
class TestCertificationErrors(unittest.TestCase):
    # This will be mutated into error cases
    # In order to avoid working on the same reference, it's gonna be copied with list()
    VALID_SAMPLE_TO_MUTATE = VALID_SAMPLE

    @data(
        [],
        ["Luc Legardeur"],
        ["Luc Legardeur", "Oui"],
        ["Luc Legardeur", "Oui", "CKAD"],
    )
    def test_missing_basic_infos(self, value):
        """
        When basic information (name, employment status, certification
        name/status) are missing, an appropriate Exception should be raised
        """
        with self.assertRaises(CertificationDeserializationError.MissingInfo):
            Certification(value)

    @data(
        ["Luc", "Oui", "CKAD", "Active"],
        ["Luc", "Oui", "CKAD", "Active", "1 janvier 2020"],
        ["Luc", "Oui", "CKAD", "Active", "1 janvier 2020", "2 janvier 2021"],
    )
    def test_missing_infos_for_active_certification(self, value):
        """
        When information about an Active certification (pass/expiration date,
        ID) are missing, an appropriate Exception should be raised.
        """
        with self.assertRaises(CertificationDeserializationError.MissingInfo):
            Certification(value)

    def test_invalid_employment_status(self):
        data = list(self.VALID_SAMPLE_TO_MUTATE)
        data[1] = "Maybe?"
        with self.assertRaises(CertificationDeserializationError.InvalidValue):
            Certification(data)

    def test_invalid_certification_status(self):
        data = list(self.VALID_SAMPLE_TO_MUTATE)
        data[3] = "Some INEXISTING status"
        with self.assertRaises(CertificationDeserializationError.InvalidValue):
            Certification(data)

    def test_expiration_date_before_obtention_date(self):
        data = list(self.VALID_SAMPLE_TO_MUTATE)
        data[4], data[5] = data[5], data[4]  # Swap obtention and expiration dates
        with self.assertRaises(CertificationDeserializationError.IncoherentValues):
            Certification(data)

    def test_invalid_obtention_date(self):
        data = list(self.VALID_SAMPLE_TO_MUTATE)
        data[4] = "An 42 de l'ère des poneys"
        with self.assertRaises(CertificationDeserializationError.InvalidObtentionDate):
            Certification(data)

    def test_invalid_expiration_date(self):
        data = list(self.VALID_SAMPLE_TO_MUTATE)
        data[5] = "Un temps que les moins de 20 ans ne peuvent pas connaître"
        with self.assertRaises(CertificationDeserializationError.InvalidExpirationDate):
            Certification(data)

    def test_invalid_certificate_id_format(self):
        data = list(self.VALID_SAMPLE_TO_MUTATE)
        data[6] = "SomeW31rdCertificate-ID"
        with self.assertRaises(
            CertificationDeserializationError.UnknownCertificateIdFormat
        ):
            Certification(data)

    # Test weird date formats
    # Test empty fields
    # Test superfluous fields (dates when InProgress, etc)


class TestCertification(unittest.TestCase):
    def test_full_valid_sample(self):
        data = list(VALID_SAMPLE)
        cert = Certification(data)

        self.assertEqual(cert.name, data[0])
        self.assertEqual(cert.currently_employed, True)
        self.assertEqual(cert.certification, data[2])
        self.assertEqual(cert.status, CertificationStatus.Active)
        self.assertEqual(cert.obtention_date, datetime.date(year=2020, month=1, day=1))
        self.assertEqual(cert.expiration_date, datetime.date(year=2023, month=1, day=2))
        self.assertEqual(cert.certificate_id.value, data[6])
        self.assertEqual(cert.certificate_id.format, CertificateIdFormat.Second)

    def test_inprogress(self):
        data = list(VALID_SAMPLE[:4])
        data[3] = "En cours de préparation"
        cert = Certification(data)

        self.assertEqual(cert.status, CertificationStatus.InProgress)

    def test_not_employed_anymore(self):
        data = list(VALID_SAMPLE)
        data[1] = "Non"
        cert = Certification(data)

        self.assertEqual(cert.currently_employed, False)

    def test_first_certificate_id(self):
        data = list(VALID_SAMPLE)
        data[6] = "CKAD-0000-123456-7890"
        cert = Certification(data)

        self.assertEqual(cert.certificate_id.value, data[6])
        self.assertEqual(cert.certificate_id.format, CertificateIdFormat.First)


# test mixed up CKA and CKAD prefix in ID
# Split errors more
# def test_preparing(self):
#     row = ["Luc Legardeur", "Oui", "CKAD", "En cours de préparation"]
#     certification = Certification(row)
#     self.assertEqual(certification.name, "Luc Legardeur")
#     self.assertEqual(certification.currently_employed, "Luc Legardeur")
