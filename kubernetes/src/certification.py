import re
import datetime
import dateparser
from enum import Enum


class CertificationDeserializationError(object):
    class InvalidValue(Exception):
        def __init__(self, name, field_desc, value, allowed):
            self.message = (
                f"Failed to deserialize {field_desc} for {name}. "
                f"Got '{value}' but expected {allowed}"
            )
            super().__init__(self.message)

    class InvalidObtentionDate(InvalidValue):
        def __init__(self, error):
            self = error  # noqa: F841

    class InvalidExpirationDate(InvalidValue):
        def __init__(self, error):
            self = error  # noqa: F841

    class MissingInfo(Exception):
        # self.message=f"Failed to deserialize {field_desc}: field is missing"
        pass

    class IncoherentValues(Exception):
        pass  # TODO raise NotImplementedError ?

    class UnknownCertificateIdFormat(Exception):
        pass


class CertificationStatus(Enum):
    Active = "Active"
    InProgress = "En cours de préparation"
    # Expired = "Expirée" # TODO introduce it


class CertificateIdFormat(Enum):
    First = r"(CKA|CKAD)-\d{4}-\d{6}-\d{4}"
    Second = r"LF-[a-z\d]{10}"


class CertificateId(object):
    """There are 2 kinds of Certificate ID:
       - Before ~June 2020: CKAD-0000-012345-0123
       - After ~June 2020: LF-a1b2c3def4
    This class represent such an ID.
    """

    def __init__(self, raw_id):
        if re.fullmatch(CertificateIdFormat.First.value, raw_id):
            self.format = CertificateIdFormat.First
        elif re.fullmatch(CertificateIdFormat.Second.value, raw_id):
            self.format = CertificateIdFormat.Second
        else:
            raise CertificationDeserializationError.UnknownCertificateIdFormat(
                f"Certificate ID {raw_id} doesn't match any known format"
            )
        self.value = raw_id
        # TODO check validity against some LF API that might exist?


class Certification(object):
    """Certification represent a given certification for a given person.

    It corresponds to the following spreadsheet fields/columns:
    - Nom
    - En poste
    - Certification
    - Statut
    - Date d'obtention
    - Date d'expiration
    - Certificate ID
    - Notes
    """

    def _parseEmploymentStatus(self, raw_string) -> bool:
        employmentStatusMap = {"Oui": True, "Non": False}
        try:
            return employmentStatusMap[raw_string]
        except KeyError as error:
            raise CertificationDeserializationError.InvalidValue(
                # fmt: off
                name        = self.name,
                field_desc  = "employment status",
                value       = raw_string,
                allowed     = employmentStatusMap.keys()
                # fmt: on
            ) from error

    def _parseCertificationStatus(self, raw_string) -> CertificationStatus:
        try:
            return CertificationStatus(raw_string)
        except ValueError as error:
            raise CertificationDeserializationError.InvalidValue(
                # fmt: off
                name        = self.name,
                field_desc  = "certification status",
                value       = raw_string,
                allowed     = [e.name for e in CertificationStatus]
                # fmt: on
            ) from error

    def _parseDate(self, raw_string, date_description) -> datetime.date:
        """_parseDate wraps dateparser.parse in order to:
        - raise an Exception in case of failure
        - return a date instead of a datetime
        """
        parsed_date = dateparser.parse(raw_string)
        if not parsed_date:
            raise CertificationDeserializationError.InvalidValue(
                # fmt: off
                name        = self.name,
                field_desc  = date_description,
                value       = raw_string,
                allowed     = "a valid date format"
                # fmt: on
            )
        return parsed_date.date()

    def _parseObtentionDate(self, raw_string):
        try:
            return self._parseDate(raw_string, "obtention date")
        except CertificationDeserializationError.InvalidValue as error:
            raise CertificationDeserializationError.InvalidObtentionDate(
                error
            ) from error

    def _parseExpirationDate(self, raw_string):
        try:
            return self._parseDate(raw_string, "expiration date")
        except CertificationDeserializationError.InvalidValue as error:
            raise CertificationDeserializationError.InvalidExpirationDate(
                error
            ) from error

    def __init__(self, infos):
        print("Initializing Certification from infos: " + str(infos))
        try:
            # fmt: off
            self.name: str                   = infos[0]
            self.currently_employed: bool    = self._parseEmploymentStatus(infos[1])
            self.certification: str          = infos[2]
            self.status: CertificationStatus = self._parseCertificationStatus(infos[3])
            # fmt: on

            if self.status == CertificationStatus.Active:
                self.obtention_date = self._parseObtentionDate(infos[4])
                self.expiration_date = self._parseExpirationDate(infos[5])
                if self.obtention_date > self.expiration_date:
                    raise CertificationDeserializationError.IncoherentValues(
                        "Obtention date cannot be _after_ the expiration date"
                    )
                self.certificate_id = CertificateId(infos[6])
        except IndexError as error:
            # TODO add details of object in error message
            raise CertificationDeserializationError.MissingInfo() from error

        print(self)

    def isOngoing(self):
        return self.status == CertificationStatus.Active and self.currently_employed

    def __str__(self):
        desc = f"{self.name} - {self.certification}: {self.status.name}\n"
        if self.isOngoing():
            desc += f"  - Obtained: {self.obtention_date}\n"
            desc += f"  - Expires: {self.expiration_date}\n"
            desc += f"  - ID: {self.certificate_id}\n"
        return desc
