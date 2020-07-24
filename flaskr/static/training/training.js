function get_learning_data_form() {
    var form_data = {}

    $("#learning_rate_params").find("input").each(function () {
        form_data[this.id] = this.value
    });

    form_data["learning_rate_function"] = $("select#learning_rate_function").val()

    return form_data;
}

function show_callback(data) {
    var image_element = "<img src='data:image/png;base64," + data.learning_graph + "' class='img-fluid'/>";
    $("div#image_learning_div").empty();
    $("div#image_learning_div" ).append(image_element);

    document.getElementById("overlay").style.display = "none";
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
        document.getElementById("overlay").style.display = "block";

        var dataAjax = JSON.stringify(get_learning_data_form());

        $.ajax({
            method: 'POST',
            contentType: "application/json;charset=utf-8",
            url: $SCRIPT_ROOT + '/training/_show_learning_function',
            data: dataAjax,
            dataType: "json",
            error: function(error){
                document.getElementById("overlay").style.display = "none";
                alert("Error in action");
            }
          }).done(show_callback);
    });

    $('button#train_model').on('click', function () {
        document.getElementById("overlay").style.display = "block";
    });
});