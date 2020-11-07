from enum import Enum

# pylint: disable=bad-super-call
class CertificationDeserializationError(object):
    class MissingInfo(Exception):
        pass
        #def __init__(self, field_desc):
        #    self.message = "Failed to deserialize {field_desc}: field is missing".format(
        #            field_desc = field_desc)
        #    super(type(self), self).__init__(self.message)
    class InvalidValue(Exception):
        def __init__(self, name, field_desc, value, allowed):
            self.message = "Failed to deserialize {field_desc} for {name}. Got '{value}' but expected {allowed}".format(
                    field_desc = field_desc,
                    name = name,
                    value = value,
                    allowed = allowed)
            super(type(self), self).__init__(self.message)


class Certification(object):
    '''Certification represent a given certification for a given person.

    It corresponds to the following spreadsheet fields/columns:
    - Nom
    - En poste
    - Certification
    - Statut
    - Date d'obtention
    - Date d'expiration
    - Certificate ID
    - Notes
    '''
    class CurrentlyEmployed(Enum):
        Oui = True
        No = False

    class CertificationStatus(Enum):
        Active = "Active"
        Preparing = "En cours de préparation"
        # Expired = "Expirée" # Not introduced yet

    def __init__(self, infos):
        try:
            self.name = infos[0]

            try:
                self.currently_employed = self.CurrentlyEmployed[infos[1]]
            except KeyError:
                raise CertificationDeserializationError.InvalidValue (
                        name        = self.name,
                        field_desc  = "employment status",
                        value       = infos[1],
                        allowed     = [e.name for e in self.CurrentlyEmployed])

            self.certification = infos[2]

            try:
                self.status = self.CertificationStatus(infos[3])
            except KeyError:
                raise CertificationDeserializationError.InvalidValue (
                        name        = self.name,
                        field_desc  = "certification status",
                        value       = infos[3],
                        allowed     = [e.name for e in self.CertificationStatus])

            if self.status == self.CertificationStatus.Active:
                self.obtention_date     = infos[4]
                self.expiration_date    = infos[5]
                self.certificate_id     = infos[6]
        except IndexError as error:
            # TODO add details of object in error message
            raise CertificationDeserializationError.MissingInfo() from error
        #, self.obtention_date, self.obtention_expiration, self.certificate_id

    #def _parseEmploymentStatus(employmentStatus):
