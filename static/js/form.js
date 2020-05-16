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
				$('#nt0').text(data.news_title_0).show();
				$('#nt1').text(data.news_title_1).show();
				$('#nt2').text(data.news_title_2).show();
				console.log('updating news');
				$('#nc0').text(data.news_content_0).show();
				$('#nc1').text(data.news_content_1).show();
				$('#nc2').text(data.news_content_2).show();

				$('#nt0').attr("href", data.news_url0);
				$('#nt1').attr("href", data.news_url1);
				$('#nt2').attr("href", data.news_url2);
				console.log('updated news!');
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});
