from flask import Flask, render_template, request
import requests, json, os


# load env variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# define env variables
weather_api = os.getenv("WEATHER_KEY")
geo_api = os.getenv("GEO_KEY")
local_ip = os.getenv("LOCAL") #local testing

# get bulk data for state name
filename = os.path.join(app.static_folder, 'city.list.json')
with open(filename) as json_file:
	bulk_data = json.load(json_file)

# get json data for country name
name_file = os.path.join(app.static_folder, 'names.json')
with open(name_file) as name_json:
	country_name = json.load(name_json)


#d = [{'city': auto_city[i], 'state': auto_state[i] } for i in range(len(auto_city))]

	
# locate user by ip address
def locate(ip_address):
	if ip_address:
		url = 'http://api.ipstack.com/'+ ip_address + '?access_key=' + geo_api + '&fields=city'
		response = requests.get(url)
		location_data = response.json()
		location = location_data['city']
		return location

	else:
		city = str('tokyo')


#load api data
@app.route('/', methods = ['POST','GET'])
def sweather():
	ip_address = str(request.environ['HTTP_X_FORWARDED_FOR']) #local_ip -- testing only

	if request.method == 'GET':
		city = request.args.get('city')
		if city is None:
			city = locate(ip_address)
		elif city == '':
			city = locate(ip_address)

	#request.form['city'] -- post method

	url = 'http://api.openweathermap.org/data/2.5/forecast?q=' + city + '&units=imperial&appid=' + weather_api

	# access the API in json format
	response = requests.get(url)

	# convert response into dictionary
	weather_data = response.json()

	# parse bulk data for state, cross referencing id in weather_data
	for i in bulk_data:
		if i['id'] == weather_data['city']['id']:
			state = i['state']
			city = i['name']

	# parse country data for full country name and ref to weather_data
	for i in country_name:
		if i == weather_data['city']['country']:
			country = country_name[i]
			print(country)

	data = {
		"state": state,
		"id": weather_data['city']['id'],
		"city": weather_data['city']['name'],
		"country": country,
		"temp_now": weather_data['list'][0]['main']['temp'],
		"humidity": weather_data['list'][0]['main']['humidity'],
		"wind": weather_data['list'][0]['wind']['speed'],
		"main": weather_data['list'][0]['weather'][0]['main'],
		"main_id": weather_data['list'][0]['weather'][0]['id'],
		"desc": weather_data['list'][0]['weather'][0]['description'].title(),
		"lat": weather_data['city']['coord']['lat'],
		"lon": weather_data['city']['coord']['lon'],
	}

	# define vars for lat and lon based on prev api call
	lat = str(data['lat'])
	lon = str(data['lon'])

	# url for one call api to get min and max temps
	min_max_url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon=" + lon + "&units=imperial&exclude=current,minutely,hourly,&appid=" + weather_api

	# access api
	min_max_response = requests.get(min_max_url)
	min_max = min_max_response.json()

	# update data with new max and min temps
	data.update({"temp_max": min_max['daily'][0]['temp']['max']})
	data.update({"temp_min": min_max['daily'][0]['temp']['min']})

	return render_template('sweather.html', data = data)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

# handle invalid searches
@app.errorhandler(KeyError)
def bad_request(e):
	return render_template('404.html'), 404

#local only 
'''
if __name__ == '__main__':
   app.run(debug = True)

'''




