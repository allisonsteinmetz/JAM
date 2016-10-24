$("#login").submit(function (event) {
    // Stop form from submitting normally
    event.preventDefault();
    var attempt = 3; // Variable to count number of attempts.
    // Below function Executes on click of login button.
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
});