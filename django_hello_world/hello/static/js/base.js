$(document).ready(function() {
        add_image_features();
        $('#edit_form').ajaxForm({
            dataType : 'json',
            beforeSend: function () {
                clear_errors();
                block_form();
                 
            },
            success: function (response) {
                $('#result').html(response.result);
                if(response.result == 'Error')
                {
                    errors = '';
                    for (error_ in response.errors)
                    {
                        errors+=response.errors[error_];
                        error_elem = '';
                        for (problem in response.errors[error_])
                        {
                            error_elem +=response.errors[error_][problem];
                        }
                        $('#error_'+error_).html('<strong>' + error_elem + '</strong><br/>');
                    }
                    
                }
                unblock_form();
            },
            error: function(response) { 
                    unblock_form(); 
                    $('#result').html('Error: data not send');
            }
        });
    });
    
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var image = document.getElementById('thumb');
                image.setAttribute('src', e.target.result);
                image.style.visibility = 'visible';
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

function add_image_features(){
    document.getElementById('id_photo').setAttribute("onchange","readURL(this);")
    };
    
function block_form(){
    $("#edit_form :input").attr("disabled", "disabled");
};

function unblock_form(){
    $("#edit_form :input").removeAttr("disabled");
};

function clear_errors(){
        $(".fieldWrapper div").empty();

};
