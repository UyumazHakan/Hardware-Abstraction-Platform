from enum import Enum
from security_communication.security import *
from security_communication.communication import *


class SecurityEnum(Enum):
	PlainText = 1
	#Asymmetric = 2


class CommunicationEnum(Enum):
	KAFKA = 1
	HTTP = 2
	MQTT = 3

security_constructors = {
	1 : PlainTextSecurityProtocol
	#2 : AsymmetricSecurityProtocol
}

communication_constructors = {
	1 : KafkaCommunicationProtocol,
	2 : HTTPCommunicationProtocol,
	3 : MQTTCommunicationProtocol
}
