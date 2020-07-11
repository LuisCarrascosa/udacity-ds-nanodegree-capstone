$(document).ready(function () {
    $('#stock_select').on('change', function (e) {
        $("[type=checkbox]").attr('disabled', false)

        if (this.value != "0") {
            $("#" + this.value).attr('disabled', true)
            // $("#" + this.value).attr('checked', false)
        }
    });

    $("#form_id").submit(function (event) {
        if ($("#stock_select").val() == "0" || $("#feature_select").val() == "0") {
            alert("Please, select a feature and a stock to predict...")
            event.preventDefault();
            return false
        }

        if (!$('[type=checkbox]').is(':checked')) {
            alert("Please, select dependent stocks for the analisys...")
            event.preventDefault();
            return false
        }

        document.getElementById("overlay").style.display = "block";

        return true;
    });

    if ($('#stock_select').val() != 0) {
        $("#" + $('#stock_select').val()).attr('disabled', true)
    }
});