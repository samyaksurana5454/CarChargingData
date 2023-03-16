import folium
import smartcar
from flask import Flask, redirect, request, jsonify, render_template
from flask_cors import CORS
from IPython.display import HTML, display

app = Flask(__name__)
CORS(app)

# define a function that takes latitude and longitude as input and returns a folium map
def create_map(latitude, longitude, icon_image_url):
    # create a custom marker icon using the car image
    car_icon = folium.features.CustomIcon(
        icon_image=icon_image_url,
        icon_size=(50, 50)
    )

    # create a folium map centered at the given latitude and longitude
    mylocation = [latitude, longitude]
    print(mylocation)
    my_map = folium.Map(mylocation, zoom_start=15)

    # add a marker for the car location using the custom marker icon
    folium.Marker(
        mylocation,
        popup='<i>Location</i>',
        icon=car_icon
    ).add_to(my_map)
    #folium.Marker(location=mylocation).add_to(my_map)

    # return the folium map object
    return my_map


# global variable to save our access_token
access = None
client = smartcar.AuthClient(
    client_id="70b19a73-d353-4822-aa78-40cf47a3e0ab",
    client_secret="5696ffe3-7ec6-4a68-ab92-9cd4196c4ab6",
    redirect_uri="https://car-charging.herokuapp.com/exchange",
    mode="test"
)

@app.route("/")
def hello_world():
    return '<p><button onclick="window.location.href=\'/login\'">Login</button></p>'

@app.route("/login", methods=["GET"])
def login():
    scope = ['read_vehicle_info', 'read_odometer', 'read_location', 'read_tires', 'read_battery', 'read_charge']
    auth_url = client.get_auth_url(scope)
    return redirect(auth_url)

# @app.route('/exchange', methods=['GET'])
# def exchange():
#     code = request.args.get('code')
#     global access
#     access = client.exchange_code(code)
#     return redirect('/vehicle')
access = None

@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')

    # TODO: Request Step 1: Obtain an access token
    # access our global variable and store our access tokens
    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    return redirect('/vehicle')

# ./main.py

@app.route('/vehicle', methods=['GET'])
# TODO: Request Step 2: Get vehicle information
def get_vehicle():
    # access our global variable to retrieve our access tokens
    global access
    # Send a request to get a list of vehicle ids
    vehicles = smartcar.get_vehicles(access.access_token)
    vehicle_ids = vehicles.vehicles
    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access.access_token)

    # Make a request to Smartcar API
    attributes = vehicle.attributes()
    odometer = vehicle.odometer()
    location = vehicle.location()
    print(access)
    pressure = vehicle.tire_pressure()
    battery=vehicle.battery()
    capacity=vehicle.battery_capacity()
    charge=vehicle.charge()

    # create a folium map object
    car_image_url = 'https://cdn4.iconfinder.com/data/icons/small-n-flat/24/map-marker-512.png'
    my_map = create_map(location.latitude, location.longitude, car_image_url)

    # convert the folium map object to HTML
    map_html = my_map._repr_html_()
    
    return render_template('vehicle.html',
                           make=attributes.make,
                           model=attributes.model,
                           year=attributes.year,
                           distance=odometer.distance,
                           latitude=location.latitude,
                           longitude=location.longitude,
                           back_left_pressure=pressure.back_left,
                           back_right_pressure=pressure.back_right,
                           front_left_pressure=pressure.front_left,
                           front_right_pressure=pressure.front_right,
                           Battery_range=battery.range,
                           percent_remaining=battery.percent_remaining,
                           battery_capacity=capacity.capacity,
                           plugged_in=charge.is_plugged_in,
                           charge_status=charge.state,


                           map_html=map_html)
    '''
    {
        "make": "TESLA",
        "model": "Model S",
        "year": 2014
    }
    '''
#     @app.route('/vehicle', methods=['GET'])
#     def get_vehicle():
#     global access
#     vehicles = smartcar.get_vehicles(access.access_token)
#     vehicle_ids = vehicles.vehicles
#     vehicle = smartcar.Vehicle(vehicle_ids[0], access.access_token)
#     attributes = vehicle.attributes()
#     odometer = vehicle.odometer()
#     location = vehicle.location()
#     print(access)
#     pressure = vehicle.tire_pressure()
#     battery=vehicle.battery()
#     capacity=vehicle.battery_capacity()
#     charge=vehicle.charge()

#     # create a folium map object
#     car_image_url = 'https://cdn4.iconfinder.com/data/icons/small-n-flat/24/map-marker-512.png'
#     my_map = create_map(location.latitude, location.longitude, car_image_url)

#     # convert the folium map object to HTML
#     map_html = my_map._repr_html_()
#     #print("samyak")
#     #print(map_html)
#     # return a JSON object with the data and the folium map as HTML
#     #return render_template('vehicle.html')
#     return render_template('vehicle.html',
#                            make=attributes.make,
#                            model=attributes.model,
#                            year=attributes.year,
#                            distance=odometer.distance,
#                            latitude=location.latitude,
#                            longitude=location.longitude,
#                            back_left_pressure=pressure.back_left,
#                            back_right_pressure=pressure.back_right,
#                            front_left_pressure=pressure.front_left,
#                            front_right_pressure=pressure.front_right,
#                            Battery_range=battery.range,
#                            percent_remaining=battery.percent_remaining,
#                            battery_capacity=capacity.capacity,
#                            plugged_in=charge.is_plugged_in,
#                            charge_status=charge.state,


#                            map_html=map_html)

@app.errorhandler(Exception)
def handle_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = 500
    return response

if __name__ == "__main__":
    app.run(port=8000)
