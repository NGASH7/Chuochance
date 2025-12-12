
var subcounty_id = $("#id_personal_details-subcounty").val();
var ward_id = $("#id_personal_details-ward").val();


var wards_url = $("#personalDetailsForm").attr("data-wards-url");

var subcounty_func = function (url, subcounty_id) {
	$.ajax({                       // initialize an AJAX request
		url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
		data: {
			'subcounty': subcounty_id       // add the country id to the GET parameters
		},
		success: function (data) {   // `data` is the return of the `load_cities` view function
			$("#id_ward").html(data);  // replace the contents of the city input with the data that came from the server
		}
	});
}

$("#id_subcounty").change(function () {
	var subcounty_id = $(this).val();
	subcounty_func(wards_url, subcounty_id);
});
