$(document).ready(function () {
    $("#button").click(function () {
      var username = document.getElementById("username").value;
      var password = document.getElementById("pwd").value;
      var destURL = 'localhost:5000/authenticate/' + username + '/' + password;
      console.log(destURL);

      $.getJSON(destURL, function(data) {
          console.log("here");
        });
        window.open("success.html"); // Redirecting to other page.
        // var attempt = 3;
        // if (username == "juicearific" && password == "demopw123") {
        //     console.log("Login Successfully!");
        // }
        // else {
        //     attempt--; // Decrementing by one.
        //     alert("You have " + attempt + " attempt left;");
        //     // Disabling fields after 3 attempts.
        //     if (attempt == 0) {
        //         document.getElementById("username").disabled = true;
        //         document.getElementById("pwd").disabled = true;
        //         document.getElementById("button").disabled = true;
        //     }
        // }
    });
});

// $(document).ready(function(){
//     $("#button").click(function(){
//       //window.open("success.html");
//       var destURL = 'localhost/authenticate/' + username + '/' + password;
//       $.ajax({
//         url: destURL,
//         dataType: "jsonp",
//         success: function(data)
//         {
//           alert("we made it!");
//         }
//       })
//     });
// });
