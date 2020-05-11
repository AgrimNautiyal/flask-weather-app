$(document).ready(function() {

	$('form').on('submit', function(event) {

    console.log('Event is Listening');
		$.ajax({
			data : {
				name : $('#CityInput').val()
			},
			type : 'POST',
			url : '/checkInput'
		})
		.done(function(data) {
			console.log('Making decision');
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#currentCity').text(data.name).show();
				$('#currentTemp').text(data.temp).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});
