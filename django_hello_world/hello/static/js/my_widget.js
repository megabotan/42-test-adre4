$(function() {
    $( "#id_date_of_birth" ).datepicker();
    var temp = $( "#id_date_of_birth" ).val();
    $( "#id_date_of_birth" ).datepicker("option", "dateFormat", "yy-mm-dd");
    $( "#id_date_of_birth" ).val(temp);
  });
