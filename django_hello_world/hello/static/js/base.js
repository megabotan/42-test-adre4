$(document).ready(function() {
        remove_broken_img();
        add_form_ajax();
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

function remove_broken_img(){
    document.getElementById('id_photo').setAttribute("onchange","readURL(this);")
    var img = document.getElementById('thumb');
    img.style.visibility = 'hidden';
    img.onerror = function () { 
    this.style.display = "none";
    };
    };
    
function block_form(){
    $("#edit_form :input").attr("disabled", "disabled");
};

function unblock_form(){
    $("#edit_form :input").removeAttr("disabled");
};

function add_form_ajax(){
    $('#edit_form').submit(function() {
            $('#result').html("Saving...");
            $.ajax({ 
                data: $(this).serialize(), 
                type: $(this).attr('method'), 
                url: $(this).attr('action'),
                beforeSend: function() { 
                    block_form(); 
                },
                success: function(response) { 
                    $('#result').html(response);
                    unblock_form(); 
                },
                error: function() { 
                    $('#result').html("Error");
                    unblock_form(); 
                }
            });
            return false;
        });
    };
