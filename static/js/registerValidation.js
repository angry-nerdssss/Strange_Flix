$("#id_username").change(function () {
    var form = $("#registration-form");
    var errormsg = document.getElementById('username-error');
    var successmsg = document.getElementById('username-success');
    // console.log(errormsg);
    $.ajax({
      url: form.attr("data-validate-username-url"),
      data: form.serialize(),
      dataType: 'json',
      success: function (data) {
        if (data.is_taken) {
        //   alert(data.error_message);
            errormsg.innerText = "*" + data.error_message;
            successmsg.innerText = "";
        }
        else{
            errormsg.innerText = "";
            successmsg.innerText = "*username valid";
        }
      }
    });
  });

