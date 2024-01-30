from flask import Flask, render_template, request, jsonify, redirect
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

app = Flask(__name__)

thresholds = {
            'temperatureMin': 15,
            'temperatureMax': 20,
            'humidityMin': 0,
            'humidityMax': 30,
            'luminanceMin': 0,
            'luminanceMax': 10,
            'gforceMin': 0,
            'gforceMax': 1
        }

inRangeImages=["static/icecream.gif",
         "static/testtubenormal.gif",
         "static/bread.jpg"]
outsideRangeImages = ["static/icecreammelt.gif",
                      "static/testtubelight.gif",
                      "static/breadfungus.jpg"]


sensorData = {}

# Create mqtt_broket_ip and store broker address in it
mqtt_broker_ip = "broker.emqx.io"  

# Define callback function on_message() with three arguments client, userdata and msg for handling incoming MQTT messages
def on_message(client, userdata, msg):
    # Access sensorData as global
    global sensorData
    # Get topic from the msg
    topic = msg.topic
    # Decode the payload
    payload = msg.payload.decode('utf-8')
    # Store payload as value at topic key in sensorData
    sensorData[topic] = payload

    # Print sensorData
    print(sensorData)
    print("mqtt : ", msg.payload.decode('utf-8') )

# Create an MQTT client instance
mqtt_client = mqtt.Client()
# Set the callback function for incoming messages
mqtt_client.on_message = on_message
# Connect to the MQTT broker
mqtt_client.connect(mqtt_broker_ip, 1883, 60)
# Subscribe to the desired MQTT topics
mqtt_client.subscribe("/Temperature")
mqtt_client.subscribe("/Humidity")
mqtt_client.subscribe("/Lux")
mqtt_client.subscribe("/Gforce")
# Start the MQTT loop to listen for incoming messages
mqtt_client.loop_start()


@app.route('/')
def index():
    global thresholds
    return render_template('index.html', thresholds=thresholds)

@app.route("/getSensorData", methods=['POST'])
def getSensorData():
    return jsonify(sensorData)

    
if __name__ == '__main__':
    app.run(debug=True)
