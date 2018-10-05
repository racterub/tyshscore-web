function check() {
	var stdid = document.getElementById("stdid");
	var passwd = document.getElementById("stdpwd");
	if (stdid.checkValidity() == true && stdpwd.checkValidity() == true) {
		document.getElementById('loading').style = '';
	}
}