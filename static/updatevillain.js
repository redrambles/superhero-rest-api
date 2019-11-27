$(document).ready(() => {
	document.getElementById("form").onsubmit = handleUpdateForm;
});

function handleUpdateForm(event) {
	event.preventDefault();
	console.log("update handler");

	var name = $("input[name='name']").val();
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
