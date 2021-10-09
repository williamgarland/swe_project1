function showLoginError(errorStr) {
    $("#error_div").html(errorStr);
}

$(function () {
    $("#log_in_button").click(function () {
        $.ajax({
            url: '/validate_login',
            data: $('#login_form').serialize(),
            type: 'POST',
            dataType: "json",
            success: function (data) {
                // The data returned will be a JSON object consisting of:
                // { valid: true|false }
                if (data.valid) {
                    window.location.href = "/";
                } else {
                    showLoginError("Error logging in - Invalid credentials");
                }
            },
            error: function (error) {
                showLoginError("Error logging in - Server unavailable");
            }
        });
    });
});
