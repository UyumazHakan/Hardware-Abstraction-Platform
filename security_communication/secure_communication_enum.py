from enum import Enum
from security_communication.security import *
from security_communication.communication import *


class SecurityEnum(Enum):
	PlainText = 1


class CommunicationEnum(Enum):
	Kafka = 1
	HTTP = 2

security_constructors = {
	1 : PlainTextSecurityProtocol
}

communication_constructors = {
	1 : KafkaCommunicationProtocol,
	2 : HTTPCommunicationProtocol
}


