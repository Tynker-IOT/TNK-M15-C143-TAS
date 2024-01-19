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

mqtt_broker_ip = "broker.emqx.io"  

def on_message(client, userdata, msg):
    global sensorData
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    sensorData[topic] = payload

    print(sensorData)
    print("mqtt : ", msg.payload.decode('utf-8') )

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker_ip, 1883, 60)
mqtt_client.subscribe("/Temperature")
mqtt_client.subscribe("/Humidity")
mqtt_client.subscribe("/Lux")
mqtt_client.subscribe("/Gforce")
mqtt_client.loop_start()


@app.route('/')
def index():
    global thresholds
    return render_template('index.html', thresholds=thresholds)

@app.route("/getSensorData", methods=['POST'])
def getSensorData():
    return jsonify(sensorData)

# Create /setThresholds post route
@app.route('/setThresholds', methods=['POST'])
# Define set_thresholds() function
def set_thresholds():
    # Access global thresholds
    global thresholds
    # Check the request method to be post
    if request.method == 'POST':
        # Get temperatureMin, temperatureMax, humidityMin, humidityMax, luminanceMin, luminanceMax, gforceMin, gforceMax from the post request and save in respective variables
        temperatureMin = request.form.get('temperatureMin')
        temperatureMax = request.form.get('temperatureMax')

        humidityMin = request.form.get('humidityMin')
        humidityMax = request.form.get('humidityMax')

        luminanceMin = request.form.get('luminanceMin')
        luminanceMax = request.form.get('luminanceMax')

        gforceMin = request.form.get('gforceMin')
        gforceMax = request.form.get('gforceMax')

        # Store every value in threshold dictionary
        thresholds = {
            'temperatureMin': temperatureMin,
            'temperatureMax': temperatureMax,
            'humidityMin': humidityMin,
            'humidityMax': humidityMax,
            'luminanceMin': luminanceMin,
            'luminanceMax': luminanceMax,
            'gforceMin': gforceMin,
            'gforceMax': gforceMax
        }

        # Redirect to "/"
        return redirect("/")
        
if __name__ == '__main__':
    app.run(debug=True)
