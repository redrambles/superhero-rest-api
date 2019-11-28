$(document).ready(() => {
	document.getElementById("form").onsubmit = handleUpdateForm;
	document.getElementById("villain-name").onchange = handleChangeSelect;
});

// Populate select element with existing villain names so we can choose one to update
$.get("/api/villains/", function(data) {
	for (let i in data) {
		$("#villain-name").append(`<option>${data[i].name}</option>`);
	}
});

function handleChangeSelect() {
	// If we have chosen a villain name - let's send a get request and populate the fields
	var name = $("select[name='name']").val();
	var desc_input = $("input[name='description']");
	var interest_input = $("input[name='interests']");
	var image_url_input = $("input[name='url']");

	if (
		$("#villain-name")
			.find(":selected")
			.data("choice") != "default"
	) {
		// Make Get request for this villain and fill out values for other fields
		$.post(
			"/api/villains/select",
			{
				name: name
			},
			function(data) {
				// data returns a jsonified dictionnary (object) at position 0 which we use to populate fields
				desc_input.val(data[0].description);
				interest_input.val(data[0].interests);
				image_url_input.val(data[0].url);
			}
		);
	} else {
		// The 'Choose a Villain' option is selected, so we need to empty out the input fields
		desc_input.val("");
		interest_input.val("");
		image_url_input.val("");
	}
}

function handleUpdateForm(event) {
	event.preventDefault();
	console.log("update handler");

	var name = $("select[name='name']").val();
	var description = $("input[name='description']").val();
	var interests = $("input[name='interests']").val();
	var url = $("input[name='url']").val();

	$.post(
		"/api/villains/update",
		{
			name: name,
			description: description,
			interests: interests,
			url: url,
			date_added: new Date()
		},
		function(data) {
			if (data.errors !== undefined) {
				document.getElementById("errors").innerHTML = data.errors
					.map(error => `<div class="error">${error}</div>`)
					.join("");
			} else {
				window.location = "/";
			}
		}
	);

	return false;
}
