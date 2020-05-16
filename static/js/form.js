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
				$('#cH').text(data.hum).show();
				$('#cW').text(data.ws).show();
				$('#news_title_0').text(data.news_content[0]['title'])
				$('#news_title_1').text(data.news_content[1]['title'])
				$('#news_title_2').text(data.news_content[2]['title'])
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});
