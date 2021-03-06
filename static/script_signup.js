function showError(errorStr) {
    $("#error_div").html(errorStr);
}

$(function () {
    $("#signup_form").on("submit", function () {
        $.ajax({
            url: '/validate_signup',
            data: $('#signup_form').serialize(),
            type: 'POST',
            dataType: "json",
            success: function (data) {
                // The data returned will be a JSON object consisting of:
                // { valid: true|false }
                if (data.valid) {
                    window.location.href = "/";
                } else {
                    showToast("Error signing up - Username already taken");
                }
            },
            error: function (error) {
                showToast("Error signing up - Server unavailable");
            }
        });
        return false;
    });
});