function check(number) {
    var reg = /^[0-9]{1,10}$/;
    var checking = reg.test(number);

    if(number.length < 10){
      alert("Please enter a valid phone number e.g 1234567890");
      return false;
    }
    else if (checking) {
      return number;
    } else {
      alert("Please enter a valid phone number e.g 1234567890");
      return false;
    }
  }


  $(document).ready(function () {
    $('#submit-text-message').click(function () {
      var message = $("#message").val();
      var number = $("#number").val();
      var name = $("#name").val();;
      console.log(message);
      console.log(number)
      console.log(name)
      console.log(email);
      var valid = check(number)
      console.log(valid)


      $.ajax({
        type: 'POST',
        url: "aws",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
          "name": name,
          "email": email,
          "number": valid,
          "message": message
        }),

      }).done(function (data) {
        console.log(data);
      });
    });
  });