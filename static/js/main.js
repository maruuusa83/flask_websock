var debug = false;
var ws = new WebSocket("ws://nado.oknctict.tk:8000/echo");

ws.onopen = function(){
	$("span#connStateIcon").attr("class", "icon-checkmark-6");
	$("span#connStateText").html("You have connection now.");
};

ws.onmessage = function(e){
	if (debug == true){
		console.log(e.data);
	}
	var recvData = jQuery.parseJSON(e.data);

	if (recvData.type == "msg"){
		str = "<blockquote style=\"width:100%;\">" + recvData.data + "</blockquote>";
		$("#view").prepend($(str));
	}
	else if (recvData.type == "err"){
		str = "<blockquote style=\"width:100%;\">" + recvData.data + "</blockquote>";
		$("#view").prepend($(str));
	}
	else if (recvData.type == "userNum"){
		$("#numOfAccess").html(recvData.data);
	}
};

ws.onclose = function(e){
	$("div#connProgress").attr("class", "");
	$("span#connStateIcon").attr("class", "icon-x");
	$("span#connStateText").html("No connection.");
};

function send_data(){
	var postDataJson = '{"type":"post", "msg":"' + $("#send_input").val() + '"';
	if ($("#send_name").val() != ""){
		splited_name = $("#send_name").val().split("#");
		postDataJson += ', "name":"' + splited_name[0] + '"';
		if (splited_name.length > 1){
			postDataJson += ', "id":"' + splited_name[1] + '"';
		}
	}

	postDataJson += '}';
	ws.send(postDataJson);
	$("#send_input").val("");
};
