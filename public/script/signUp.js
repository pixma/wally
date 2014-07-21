


$(function() {
		
	
});


$("#signUpSubmit").on('click', function(){
	
	var isFormValid = true;
	
	if( !(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test($("#signUpEmail").val())) )
	{
		//email format is wrong.
		$("#signUpEmail").popover();
		$("#signUpEmail").popover('show');
		isFormValid = false;
	}
	if(  ($("#signUpPassword").val().length < 7) ){
		
		$("#signUpPassword").popover();
		$("#signUpPassword").popover('show');
		isFormValid = false;
		
	}
	if( $("#signUpFirstName").val().length == 0){
		$("#signUpFirstName").popover();
		$("#signUpFirstName").popover('show');
		isFormValid = false;
	}
	
	if( $("#signUpLastName").val().length == 0){
		$("#signUpLastName").popover();
		$("#signUpLastName").popover('show');
		isFormValid = false;
	}
	
	if( isFormValid == false ){
		return;
	}
	else{
		// form is valid now.
		emailString = $("#signUpEmail").val();
		passwdString = $("#signUpPassword").val();
		firstNameString = $("#signUpFirstName").val();
		lastNameString = $("#signUpLastName").val();
		$.post("/signUp/", {email:emailString,
							password:passwdString,
							firstName:firstNameString,
							lastName:lastNameString})
			.done(function(data){
				if( data['success'] == true){
					$("#signUpSuccessModal").modal({
						keyboard: false,
						show : true
					});
				}
				else{
					$("#signUpFailModal").modal({
						keyboard: false,
						show : true
					});
					$("#failReason").html( data['failReason'] );
				}
			})
	}
	
	
	
});