$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-base .modal-content").html("");
        $("#modal-base").modal("show");
      },
      success: function (data) {
        $("#modal-base .modal-content").html(data.html_form);

        //refresh the selectpicker in modal to display it
        $(document).ready(function() {
            $(".selectpicker").selectpicker();
        });

      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    var formData = new FormData(form[0]);
    $.ajax({
      url: form.attr("action"),
//      data: form.serialize(),
      data: formData,
      type: form.attr("method"),
      dataType: 'json',
      async: true,
      cache: false,
      contentType: false,
      enctype: form.attr("enctype"),
      processData: false,
      success: function (data) {
        if (data.form_is_valid) {
          $("#ajax-table tbody").html(data.html_data_list);
          $("#modal-base").modal("hide");
        }
        else {
          $("#modal-base .modal-content").html(data.html_form);
        }

//refresh the selectpicker in modal to display it
    $(document).ready(function() {
        $(".selectpicker").selectpicker();
    });


      }
    });
    return false;
  };


  /* Binding */

  // Create host
  $(".js-create-host").click(loadForm);
  $("#modal-base").on("submit", ".js-host-create-form", saveForm);

  // Create inv
  $(".js-create-inv").click(loadForm);
  $("#modal-base").on("submit", ".js-inv-create-form", saveForm);

  // Create evidence
  $(".js-create-ev").click(loadForm);
  $("#modal-base").on("submit", ".js-ev-create-form", saveForm);

  // Create Investigation evidence
  $(".js-create-invev").click(loadForm);
  $("#modal-base").on("submit", ".js-invev-create-form", saveForm);


  // Update host
  $("#ajax-table").on("click", ".js-update-host", loadForm);
  $("#modal-base").on("submit", ".js-host-update-form", saveForm);

  // Update Investigation Evidence
  $("#ajax-table").on("click", ".js-update-invev", loadForm);
  $("#modal-base").on("submit", ".js-invev-update-form", saveForm);

  // Delete host
  $("#ajax-table").on("click", ".js-delete-host", loadForm);
  $("#modal-base").on("submit", ".js-host-delete-form", saveForm);


});



//###### backup
//  var saveForm = function () {
//    var form = $(this);
//    $.ajax({
//      url: form.attr("action"),
//      data: form.serialize(),
//      type: form.attr("method"),
//      dataType: 'json',
//      success: function (data) {
//        if (data.form_is_valid) {
//          $("#ajax-table tbody").html(data.html_data_list);
//          $("#modal-base").modal("hide");
//        }
//        else {
//          $("#modal-base .modal-content").html(data.html_form);
//        }