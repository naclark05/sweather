$(document).ready(function() {
	// when element is changed
	$('#celsius').change(function() {
		// convert temps to cels and round to 2 decimal places
		var tempNowCels = Math.round((tempNow - 32) * (5/9) * 100) / 100;
		var tempMaxCels = Math.round((tempMax - 32) * (5/9) * 100) / 100;
		var tempMinCels = Math.round((tempMin - 32) * (5/9) * 100) / 100;
		var windSpeedKm = Math.round((windSpeed * 1.60934) * 100) / 100;
		// if element is checked, replace text with converted data as a string
		if (this.checked) {
			$('#tempNow').text(tempNowCels.toString() + ' C');
			$('#tempMax').text(tempMaxCels.toString() + ' C');
			$('#tempMin').text(tempMinCels.toString() + ' C');
			$('#windSpeed').text(windSpeedKm.toString() + ' kmh');

		// else, use original data as a string
		} else {
			$('#tempNow').text(tempNow.toString() + ' F');
			$('#tempMax').text(tempMax.toString() + ' F');
			$('#tempMin').text(tempMin.toString() + ' F');
			$('#windSpeed').text(windSpeed.toString() + ' mph');
		}
	});

});





