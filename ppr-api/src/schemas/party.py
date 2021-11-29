import datetime
import enum

import pydantic


class PartyType(enum.Enum):
    REGISTERING = 'RP'
    SECURED = 'SP'
    DEBTOR = 'DE'


class IndividualName(pydantic.BaseModel):  # pylint:disable=no-member
    first: str
    middle: str = None
    last: str


class Address(pydantic.BaseModel):  # pylint:disable=no-member
    street: str
    streetAdditional: str = None
    city: str
    region: str = None
    country: str
    postalCode: str


class Party(pydantic.BaseModel):  # pylint:disable=no-member
    personName: IndividualName = None
    businessName: str = None
    address: Address = None

    @pydantic.validator('address', pre=None, always=True)
    def check_party_for_business_name(cls, v, values, **kwargs):  # pylint:disable=no-self-argument # noqa: N805
        if values['personName'] is None and values['businessName'] is None:
            raise KeyError('"Party" must have personName or businessName')
        return v


class Debtor(Party):
    birthdate: datetime.date = None
