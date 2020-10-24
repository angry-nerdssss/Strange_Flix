const form = $("#registration-form");
const usernameError = document.getElementById('username-error');
const usernameSuccess = document.getElementById('username-success');
const emailError = document.getElementById('email-error');
const emailSuccess = document.getElementById('email-success');
const regSubmitButton = document.getElementById('id_reg_submit');
$("#id_username").change(function () {
    $.ajax({
      url: form.attr("data-validate-username-url"),
      data: form.serialize(),
      dataType: 'json',
      success: function (data) {
        if (data.is_username_taken) {
        //   alert(data.error_message);
            usernameError.innerText = "*" + data.username_error_message;
            usernameSuccess.innerText = "";
        }
        else{
            usernameError.innerText = "";
            usernameSuccess.innerText = "*username valid";
        }
        if(data.is_username_taken || data.is_email_taken){
          regSubmitButton.disabled = true;
        }else{
          regSubmitButton.disabled = false;
        }
      }
    });
  });

$("#id_email").change(function(){
  $.ajax({
    url: form.attr("data-validate-username-url"),
    data: form.serialize(),
    dataType: 'json',
    success: function (data) {
      if (data.is_email_taken) {
        //   alert(data.error_message);
          emailError.innerText = "*" + data.email_error_message;
          emailSuccess.innerText = "";
      }
      else{
          emailError.innerText = "";
          emailSuccess.innerText = "*email valid";
      }
      if(data.is_username_taken || data.is_email_taken){
        regSubmitButton.disabled = true;
      }else{
        regSubmitButton.disabled = false;
      }
    }
  });
})