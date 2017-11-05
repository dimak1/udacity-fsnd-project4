$(document).ready(function() {
    $("#datepicker").datepicker({
        dateFormat: "yy-mm-dd",
        maxDate: "-18Y"
    });

    if ((userName == 'null') || (userName == '')) {
        hide.signoutButton();
    } else {
        hide.signinButton();
    }
});

function signInCallback(authResult) {

    $.get("/getState", function(data) {

        if (authResult['code']) {

            hide.signinButton();
            // Send the one-time-use code to the server, if the server responds, write a 'login successful' message to the web page and then redirect back to the main restaurants page
            $.ajax({
                type: 'POST',
                url: '/gconnect?state=' + data,
                processData: false,
                contentType: 'application/octet-stream; charset=utf-8',
                data: authResult['code'],
                success: function(signedInUser, textStatus) {
                    // Handle or verify the server response if necessary.
                    if (signedInUser) {
                        $('#loggedInUser').html(JSON.parse(signedInUser))
                        show.loggedInUser();
                        show.signoutButton();
                        $('.sign-in-msg').html(
                            '<div class="alert alert-primary alert-dismissible fade show text-center" role="alert">Welcome, <strong>' +
                            JSON.parse(signedInUser) + '</strong>! You are now signed in with Google!' +
                            '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                            '<span aria-hidden="true">&times;</span></button></div>');
                    } else if (authResult['error']) {
                        console.log('There was an error: ' + authResult['error']);
                        $('.sign-in-msg').html(
                            '<div class="alert alert-danger alert-dismissible fade show text-center" role="alert">' +
                            'Failed to sign in. Try again later.' +
                            '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                            '<span aria-hidden="true">&times;</span></button></div>');
                    } else {
                        $('.sign-in-msg').html(
                            '<div class="alert alert-danger alert-dismissible fade show text-center" role="alert">' +
                            'Failed to make a server-side call. Check your configuration and console.' +
                            '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                            '<span aria-hidden="true">&times;</span></button></div>');
                    }
                }
            });
        }
    });
}

function disconnect() {

    $.ajax({
        type: 'GET',
        url: '/gdisconnect',
        contentType: 'application/octet-stream; charset=utf-8',
        cache: false,
        success: function(data, textStatus) {
            console.log("Diconnecting.");
            hide.signoutButton();
            hide.loggedInUser();
            show.signinButton();
            $('.sign-in-msg').html(
                '<div class="alert alert-primary alert-dismissible fade show text-center" role="alert">Successfully signed out!' +
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                '<span aria-hidden="true">&times;</span></button></div>');
        },
        error: function(data, textStatus) {
            console.log("Error while disconneting.");
            $('.sign-in-msg').html(
                '<div class="alert alert-danger alert-dismissible fade show text-center" role="alert">' +
                'Failed to sign out. Please try again.' +
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                '<span aria-hidden="true">&times;</span></button></div>');
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
