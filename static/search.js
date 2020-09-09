// call randomColor.js 
const colors = randomColor({
	count: 3,
	luminosity: 'light'
});

// load body and use randomColor to generate colors for bg gradient
// bg color gradient changes on refresh
window.onload = function() {
	document.body.style.backgroundImage = "linear-gradient(to bottom, " + colors[0] + ", " + colors[1] + ")";
}

// ajax to convert temps to celsius
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
			$('#tempNow').text(' '+ tempNowCels.toString() + '  \u00B0C');
			$('#tempMax').text(' ' + tempMaxCels.toString() + '  \u00B0C');
			$('#tempMin').text(' ' + tempMinCels.toString() + '  \u00B0C');
			$('#windSpeed').text(' ' + windSpeedKm.toString() + ' kmh');

		// else, use original data as a string
		} else {
			$('#tempNow').text(' ' + tempNow.toString() + '  \u00B0F');
			$('#tempMax').text(' ' + tempMax.toString() + '  \u00B0F');
			$('#tempMin').text(' ' + tempMin.toString() + '  \u00B0F');
			$('#windSpeed').text(' ' + windSpeed.toString() + ' mph');
		}
	});
})







