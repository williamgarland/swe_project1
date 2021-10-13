function showLoginError(errorStr) {
    $("#error_div").html(errorStr);
}

$(function () {
    $("#login_form").on("submit", function () {
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
                    showToast("Error logging in - Invalid credentials");
                }
            },
            error: function (error) {
                showToast("Error logging in - Server unavailable");
            }
        });
        return false;
    });
});
