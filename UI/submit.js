$(document).ready(function(){
  var uName = document.getElementById("username").value;
  var password = document.getElementById("pwd").value;
    $("#button").click(function(){
      $.ajax({
        type: "POST",
        url: "~/GitHubCommunicator.py",
        data: {uName: password}
      }).done(function( o ) {

      });
        window.open("success.html");
    });
});


var attempt = 2;

function validate() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("pwd").value;
    if (username == "Formget" && password == "formget#123") {
        alert("Login successfully");
        window.open = "success.html"; // Redirecting to other page.
        return false;
    }
    else {
        attempt--; // Decrementing by one.
        alert("You have " + attempt + " attempt left;");
        // Disabling fields after 3 attempts.
        if (attempt == 0) {
            document.getElementById("username").disabled = true;
            document.getElementById("pwd").disabled = true;
            document.getElementById("button").disabled = true;
            return false;
        }
    }
}
