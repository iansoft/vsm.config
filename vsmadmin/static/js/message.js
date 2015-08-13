function ShowMessage(container,type,msg){
	var message_html = "";
	message_html += "<div class='alert {0} alert-dismissible' role='alert'>";
	message_html += "	<button type='button' class='close' data-dismiss='alert' aria-label='Close'>";
	message_html += "	<span aria-hidden='true'>&times;</span> ";
	message_html += "	</button>";

	message_html += "	<span>";
	message_html += msg;
	message_html += "	</span>";
	message_html += "</div>";

	switch(type){
		case 0: //error
			message_html = message_html.replace("{0}","alert-danger");
			break;
		case 1: //warning
			message_html = message_html.replace('{0}',"alert-warning");
			break;
		case 2: //success
			message_html = message_html.replace("{0}","alert-success");
			break;
	}
	container.empty();
	container.append(message_html);
}