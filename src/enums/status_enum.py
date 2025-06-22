from enum import Enum

class StatusPesananEnum(str, Enum):
    PENDING = 'pending'
    DIPROSES = 'diproses'
    SELESAI = 'selesai'

class StatusMenuEnum(str, Enum):
    TERSEDIA = 'TERSEDIA'
    HABIS = 'HABIS'