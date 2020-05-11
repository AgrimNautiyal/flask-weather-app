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

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#currentCity').text(data.name).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});
