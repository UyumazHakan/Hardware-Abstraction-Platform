from enum import Enum
from .security import *
from .communication import *

security_constructors = {
	1 : PlainTextSecurityProtocol
}

communication_constructors = {
	1 : KafkaCommunicationProtocol
}

class SecurityEnum(Enum):
	PlainText = 1


class CommunicationEnum(Enum):
	Kafka = 1