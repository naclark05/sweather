from flask import Flask, render_template, request
import requests, json, os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


weather_api = os.getenv("WEATHER_KEY")
geo_api = os.getenv("GEO_KEY")
local_ip = os.getenv("LOCAL") #local testing


def locate(ip_address):
	try:
		url = 'http://api.ipstack.com/'+ ip_address + '?access_key=' + geo_api + '&fields=city'
		print(url)
		response = requests.get(url)
		location_data = response.json()
		location = location_data['city']
		print(location)
		return location

	except Exception as e:
		return "new york"



#load api data
@app.route('/', methods = ['POST','GET'])
def sweather():
	ip_address = str(request.environ['HTTP_X_FORWARDED_FOR'])
	print(ip_address)
	if request.method == 'POST':
		city = request.form['city']

	else:
		city = locate(ip_address)


	url = 'http://api.openweathermap.org/data/2.5/forecast?q=' + city + '&units=imperial&appid=' + weather_api

	# access the API in json format
	response = requests.get(url)

	# convert response into dictionary
	weather_data = response.json()

	data = {
		"city": weather_data['city']['name'],
		"country": weather_data['city']['country'],
		"temp_now": weather_data['list'][0]['main']['temp'],
		"temp_min": weather_data['list'][0]['main']['temp_min'],
		"temp_max": weather_data['list'][0]['main']['temp_max'],
		"humidity": weather_data['list'][0]['main']['humidity'],
		"wind": weather_data['list'][0]['wind']['speed'],
		"clouds": weather_data['list'][0]['clouds']['all'],
		"dt": weather_data['list'][0]['dt_txt'],
	}


	return render_template('sweather.html', data = data)


#local only
#if __name__ == '__main__':
#   app.run(debug = True)









