$(function () {
    $("#search_input_form").on("submit", function () {
        var text = $("#search_input").val();
        $.ajax({
            url: "/search",
            type: "get",
            data: { search_input: text },
            success: function (response) {
                $("#search_results").html(response);
            },
            error: function (xhr) { }
        });
        return false;
    });
});