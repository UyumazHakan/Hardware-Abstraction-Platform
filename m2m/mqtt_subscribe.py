import paho.mqtt.client as paho
import sys


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))


def main(ip, port, topic):
    client = paho.Client()
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect(ip, port)
    client.subscribe(topic, qos=1)
    client.loop_forever()


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1], sys.argv[2])
