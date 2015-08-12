var config = {
    controller:"",
    nodes:[]
};


$(document).ready(function(){
	//log the config data
	console.log("log the config data");
	console.log(config);

	$("#btnSubmitConfig").click(function(){
		setConfiguration();
	})
});


function setConfiguration(){
    var token = $("input[name=csrfmiddlewaretoken]").val();
    
    //check the config controller IP
    var _Cluster_IP = $("#txtClusterAddress").val();
    if(checkIP(_Cluster_IP) == false){
    	$("#divWarning").show();
		$("#lblWarningMsg")[0].innerHTML = "The cluster address format is wrong!";
		return false;
    }
    
    //check the nodes IPs should not empty
    if($("#ulNodes>li>.node-ip").length == 0){
    	$("#divWarning").show();
		$("#lblWarningMsg")[0].innerHTML = "The node address is empty!";
		return false;
    }

    //set the datas
    config.controller = _Cluster_IP;
    $("#ulNodes>li>.node-ip").each(function(){
    	var _ip = this.innerHTML;
    	config.nodes.push(_ip);
    });

    console.log(config);


    $.ajax({
        type: "post",
        url: "/config/setconfig/",
        data: JSON.stringify(config),
        dataType:"json",
        success: function(data){
        	if(data.status == 0){
        		window.location.href = "/manifest/";
        	}
            console.log(data);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
           if(XMLHttpRequest.status == 500){
               $("#divWarning").show();
			   $("#lblWarningMsg")[0].innerHTML = "INTERNAL SERVER ERROR";
           }
        },
        headers: {
            "X-CSRFToken": token
        },
        complete: function(){

        }
    });
}


function addNode(){
	var _node_ip = $("#txtNodeAddress").val();

	//check the ip exsit or not
	var _is_exsit = false;
	$("#ulNodes>li>.node-ip").each(function(){
		var _ip = this.innerHTML;
		if(_ip == _node_ip){
			_is_exsit = true;
		}
	});
	if(_is_exsit == true){
		$("#divWarning").show();
		$("#lblWarningMsg")[0].innerHTML = "The node address is exsit!";
		return false;
	}


	//check the ip address format
	if(checkIP(_node_ip)==false){
		$("#divWarning").show();
		$("#lblWarningMsg")[0].innerHTML = "The node address format is wrong!";
	}
	else{
		$("#divWarning").hide();
		$("#lblWarningMsg")[0].innerHTML = "";

		var _html_ip_address = "";
		_html_ip_address += "<li>";
		_html_ip_address += "<span class='node-ip'>"+_node_ip+"</span>";
		_html_ip_address += "<img class='remove' src='/static/images/remove.png' onclick='removeNode(this);'>";
		_html_ip_address += "</li>";

		$("#ulNodes").append(_html_ip_address);
		// config.nodes.push(_node_ip);
		// console.log(config);
	}
	return false;
}

function clearNode(){
	$("#ulNodes").empty();
	return false;
}

function removeNode(obj){
	obj.parentNode.remove();
}