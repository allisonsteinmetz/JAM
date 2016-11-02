$(document).ready(function () {
    $("#button").click(function () {
        var attempt = 3;
        var username = document.getElementById("username").value;
        var password = document.getElementById("pwd").value;
        if (username == "mvp" && password == "mvp123") {
            console.log("Login Successfully!");
            window.open("success.html"); // Redirecting to other page.
        }
        else {
            attempt--; // Decrementing by one.
            alert("You have " + attempt + " attempt left;");
            // Disabling fields after 3 attempts.
            if (attempt == 0) {
                document.getElementById("username").disabled = true;
                document.getElementById("pwd").disabled = true;
                document.getElementById("button").disabled = true;
            }
        }
        $.ajax({
            url: "GitHubCommunicator.py"
            ,type: "POST"
            , success: function (response) {
                console.log(JSON.stringify(response));
            }
            , error: function (xhr, errmsg, err) {
                console.log("errmsg");
            }
        });
    });
});