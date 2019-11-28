$(document).ready(() => {
	document.getElementById("form").onsubmit = handleDeleteForm;
});

$.get("/api/villains/", function(data) {
	for (let i in data) {
		$("#villain-name").append(`<option>${data[i].name}</option>`);
	}
});

function handleDeleteForm(event) {
	event.preventDefault();
	var name = $("select[name='name']").val();
	$.post(
		"/api/villains/delete",
		{
			name: name
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
