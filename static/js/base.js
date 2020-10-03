window.addEventListener("scroll", function(event) { 
  
    var scroll_y = this.scrollY; 

    // console.log(scroll_y);
    
    if(scroll_y < 100){
        document.querySelector(".dark-bar").style.backgroundColor = "black";
    }else{
        document.querySelector(".dark-bar").style.backgroundColor = "rgba(0, 0, 0, 0.4)";
    }
}); 

// hideLoginForm();

function hideBothForm(){
    $(".login-form-container")[0].style.visibility = "hidden";
    console.log("loginform hidden");
    $(".registration-form-container")[0].style.visibility = "hidden";
    console.log("regform hidden");
}

function showLoginForm() {
    hideBothForm();
    $(".login-form-container")[0].style.visibility = "visible";
    console.log("loginform visible");
}


function showRegisterationForm(){
    hideBothForm();
    $(".registration-form-container")[0].style.visibility = "visible";
    console.log("regform visible");
}