from enum import Enum


class DetectionType(str, Enum):
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    CARD = "CARD"

    IPV4 = "IPV4"
    IPV6 = "IPV6"
    MAC = "MAC"
    UUID = "UUID"
    IBAN = "IBAN"
    SSN = "SSN"

    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    ADDRESS = "ADDRESS"
    DATE = "DATE"
    URL = "URL"
    PASSPORT = "PASSPORT"

    DRIVER_LICENSE = "DRIVER_LICENSE"
    MEDICAL_LICENSE = "MEDICAL_LICENSE"
    NRP = "NRP"
    UNKNOWN = "UNKNOWN"
