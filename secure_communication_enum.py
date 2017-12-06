from enum import Enum

security_constructors = {
	#1 : PlainTextSecurityProtocol
}

class SecurityEnum(Enum):
	PlainText = 1


class CommunicationEnum(Enum):
	Kafka = 1