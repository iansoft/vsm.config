$(document).ready(function(){
	//init the data
	InitData();

	$("#btnSaveClusterBasic").click(function(){
		SaveClusterBasic();
	});
});


function InitData(){
	var _Selected_File_System = $("#hfFileSystem").val();
	var _Sel_File_System = $("#selFileSystem")[0];
	for(var i=0;i<_Sel_File_System.options.length;i++){
		if(_Sel_File_System.options[i].text == _Selected_File_System){
			_Sel_File_System.options[i].selected = true;
		}
	}
}

function SaveClusterBasic(){
	//check the management address
	var _Management_Address = $("#lblManagementAddress").val();
	if(checkIPWithPort(_Management_Address)==false){
		$("#divBasicWarning").show();
		$("#divBasicSuccess").hide();
		$("#lblBasicWarningMsg")[0].innerHTML = "The management address format is wrong!";
		return false;
	}

	//check the ceph public address
	var _Ceph_Public_Address = $("#lblCephPublicAddress").val();
	if(checkIPWithPort(_Ceph_Public_Address)==false){
		$("#divBasicWarning").show();
		$("#divBasicSuccess").hide();
		$("#lblBasicWarningMsg")[0].innerHTML = "The ceph public address format is wrong!";
		return false;
	}

	//check the ceph cluster address
	var _Ceph_Cluster_Address = $("#lblCephClusterAddress").val();
	if(checkIPWithPort(_Ceph_Cluster_Address)==false){
		$("#divBasicWarning").show();
		$("#divBasicSuccess").hide();
		$("#lblBasicWarningMsg")[0].innerHTML = "The ceph cluster address format is wrong!";
		return false;
	}

	var cluster_basic_data = {
		"cluster":$("#txtCluster").val(),
		"file_system":$("#selFileSystem").val(),
		"management_addr":_Management_Address,
		"ceph_public_addr":_Ceph_Public_Address,
		"ceph_cluster_addr":_Ceph_Cluster_Address,
	};


	var token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
        type: "post",
        url: "/manifest/set_cluster_basic_file/",
        data: JSON.stringify(cluster_basic_data),
        dataType:"json",
        success: function(data){
        	$("#divBasicSuccess").show();
        	$("#divBasicWarning").hide();
			$("#lblBasicSuccessMsg")[0].innerHTML = "Save the cluster basic info. successfully!";
            console.log(data);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
           if(XMLHttpRequest.status == 500){
               $("#divBasicWarning").show();
			   $("#lblBasicWarningMsg")[0].innerHTML = "INTERNAL SERVER ERROR";
           }
        },
        headers: {
            "X-CSRFToken": token
        },
        complete: function(){

        }
    });
}

