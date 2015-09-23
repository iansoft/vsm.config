$(function(){
	$("#lblInstallMark").hide();

	$("#txtLogContainer")[0].innerHTML = $("#hfHiddenLog").val();

	$("#id_file").change(function(){
		$("#lblFileName")[0].innerHTML = $("#id_file").val();
	});

	$("#btnInstall").click(function(){
		$("#lblInstallMark").show();
	});
})

