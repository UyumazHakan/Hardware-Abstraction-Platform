from enum import Enum
from device import *


device_constructors ={
	1 : KY_01,
	2 : KY_02,
	3 : KY_03,
	10 : KY_10,
        13 : KY_13,
        15 : KY_15,
	17 : KY_17,
        20 : KY_20,
        21 : KY_21,
	24 : KY_24,
	25 : KY_25,
	26 : KY_26,
        28 : KY_28,
	31 : KY_31,
	32 : KY_32,
	33 : KY_33,
        35 : KY_35,
	36 : KY_36,
	37 : KY_37,
	50 : KY_50,
	51 : WEATHER2_BOARD,
        52 : KY_52
}

class DeviceEnum(Enum):
	KY01 = 1
	KY02 = 2
	KY03 = 3
	KY04 = 4
	KY05 = 5
	KY06 = 6
	KY07 = 7
	KY08 = 8
	KY09 = 9
	KY10 = 10
	KY11 = 11
	KY12 = 12
	KY13 = 13
	KY14 = 14
	KY15 = 15
	KY16 = 16
	KY17 = 17
	KY18 = 18
	KY19 = 19
	KY20 = 20
	KY21 = 21
	KY22 = 22
	KY23 = 23
	KY24 = 24
	KY25 = 25
	KY26 = 26
	KY27 = 27
	KY28 = 28
	KY29 = 29
	KY30 = 30
	KY31 = 31
	KY32 = 32
	KY33 = 33
	KY34 = 34
	KY35 = 35
	KY36 = 36
	KY37 = 37
	KY38 = 38
	KY39 = 39
	KY40 = 40
	KY41 = 41
	KY42 = 42
	KY43 = 43
	KY44 = 44
	KY45 = 45
	KY46 = 46
	KY47 = 47
	KY48 = 48
	KY49 = 49
	KY50 = 50
	WEATHER2BOARD = 51
	KY52 = 52

