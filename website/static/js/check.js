function check() {
	var stdid = document.getElementById("stdid");
	var passwd = document.getElementById("stdpwd");
	console.log(stdid.checkValidity())
	console.log(stdpwd.checkValidity())
	if (stdid.checkValidity() == true && stdpwd.checkValidity() == true) {
		console.log(stdid);
		console.log(stdpwd);
		document.getElementById('loading').style = '';
	}
}