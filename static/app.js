$(document).ready(function() {
    $("#datepicker").datepicker({
        dateFormat: "yy-mm-dd",
        maxDate: "-18Y"
    });

    console.log(logged);
    // console.log("State: " + state);

    if ((logged == 'null') || (logged == '')) {
        hide.signoutButton();
    } else {
        hide.signinButton();
    }

});

function signInCallback(authResult) {

    var state;

    $.get("/getState", function(data) {
        state = data;
        console.log("State: " + state);

        if (authResult['code']) {
            // Hide the sign-in button now that the user is authorized
            // $('#signinButton').attr('style', 'display: none');

            hide.signinButton();

            // Send the one-time-use code to the server, if the server responds, write a 'login successful' message to the web page and then redirect back to the main restaurants page
            $.ajax({
                type: 'POST',
                url: '/gconnect?state=' + state,
                processData: false,
                contentType: 'application/octet-stream; charset=utf-8',
                data: authResult['code'],
                success: function(data, textStatus) {
                    console.log(data);
                    console.log(textStatus);
                    // Handle or verify the server response if necessary.
                    if (data) {
                        // $('#result').html('Login Successful!</br>' + result + '</br>')
                        $('#loggedInUser').html(JSON.parse(data))
                        show.loggedInUser();
                        show.signoutButton();
                        // setTimeout(function() {
                        //     window.location.href = "/home";
                        // }, 4000);

                    } else if (authResult['error']) {
                        console.log('There was an error: ' + authResult['error']);
                    } else {
                        $('#result').html('Failed to make a server-side call. Check your configuration and console.');
                    }
                }
            });
        }
    });
}

function disconnect() {
    console.log("Diconnecting...");

    $.ajax({
        type: 'GET',
        url: '/gdisconnect',
        contentType: 'application/octet-stream; charset=utf-8',
        cache: false,
        success: function(data, textStatus) {
            console.log(data);
            console.log(textStatus);
            hide.signoutButton();
            hide.loggedInUser();
            show.signinButton();
            // Handle or verify the server response if necessary.
            // if (result) {
            //     // $('#result').html('Login Successful!</br>' + result + '</br>')
            //     $('#logged-in-user').html('Welcome, ' + result)
            //     // setTimeout(function() {
            //     //     window.location.href = "/home";
            //     // }, 4000);
            //
            // } else if (authResult['error']) {
            //     console.log('There was an error: ' + authResult['error']);
            // } else {
            //     $('#result').html('Failed to make a server-side call. Check your configuration and console.');
            // }
        },
        error: function(data, textStatus) {
            console.log("Error");
        }

    });
}

var hide = {
    loggedInUser: function() {
        $('#loggedInUser').hide();
    },
    signoutButton: function() {
        $('#signoutButton').hide();
    },
    signinButton: function() {
        $('#signinButton').hide();
    }
}

var show = {
    loggedInUser: function() {
        $('#loggedInUser').show();
    },
    signoutButton: function() {
        $('#signoutButton').show();
    },
    signinButton: function() {
        $('#signinButton').show();
    }
}
