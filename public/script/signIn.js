

$("#submitButton").on('click', function() {
	
	var isValidated = true;
	
	if( !(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test($("#email").val())) ){
		// email address or say user name is typed in wrong format.
		$("#email").popover();
		$("#email").popover('show');
		isValidated = false;
	}
	
	if(  ($("#password").val().length < 7) ){
		
		$("#password").popover();
		$("#password").popover('show');
		isValidated = false;		
	}
	
	if( isValidated == false ){
		return;
	}
	//If this passes means form is validated.
	emailUserName = $("#email").val();
	passwd = $("#password").val();
	$.post("/signIn/", {email:emailUserName, password:passwd})		
		.done( function(data) {
			if( data['LogIn'] == false ){
				$("#signInFailModal").modal({
						keyboard: true,
						show : true
					});
			}
			else if( data['LogIn'] == true ){
				routeLink = "/user/dashboard/".concat( emailUserName );
				window.location.replace(routeLink);
			}
			
		});
} );