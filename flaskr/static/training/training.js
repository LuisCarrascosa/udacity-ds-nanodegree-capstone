function get_learning_data_form() {
    var form_data = []
    $("#learning_rate_params").find("input").each(function () {
        data = {}
        data.id = this.id;
        data.value = this.value;
        form_data.push(data);
    });

    return form_data;
}

$(document).ready(function () {
    $('select#learning_rate_function').on('change', function () {
        $.getJSON($SCRIPT_ROOT + '/training/_learning_function', {
            learning_function_selected: $('select#learning_rate_function').val()
        }, function (data) {
            $("#learning_rate_params").find("input").each(function () {
                if (this.id in data.params) {
                    $(this).attr("disabled", false)
                } else {
                    $(this).attr("disabled", true)
                }
            });
        });
    });

    $('button#show_learning_function').on('click', function () {
        $.getJSON(
            $SCRIPT_ROOT + '/training/_show_learning_function',
            {form_data: get_learning_data_form()},
            function (data) {
                alert(data.num_cycles)
            }
        );
    });
});