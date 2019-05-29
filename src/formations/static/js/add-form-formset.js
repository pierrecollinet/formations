$('#empty-row').hide();
function updateEmptyFormIDs(element, totalForms){
    var thisInput = element
    // get current form input name
    var currentName = element.attr('name')
    // replace "prefix" with actual number
    var newName = currentName.replace(/__prefix__/g, totalForms)

    // update input with new name
    thisInput.attr('name', newName)
    thisInput.attr('id', "id_" + newName)
    // create a new form row id
    var newFormRow = element.closest(".form-row");
    var newRowId =  "row_id_" + newName
    newFormRow.attr("id", newRowId)
    // add new class for basic graphic animation
    newFormRow.addClass("new-parent-row")
    // update form group id
    var parentDiv = element.parent();
    parentDiv.attr("id", "parent_id_" + newName)
    // update label id
    var inputLabel = parentDiv.find("label")
    inputLabel.attr("for", "id_" + newName)

    // return created row
    return newFormRow
}
$('.add-new-form').click(function(e) {
    e.preventDefault()
    // form id like #id_form-TOTAL_FORMS
    var formId = "id_creer_lecon-TOTAL_FORMS"
    // copy empty form
    var emptyRow = $("#empty-row").clone();
    // remove id from new form
    emptyRow.attr("id", null)
    // Insert row after last row
    // get starting form count for formset
    var totalForms = parseInt($('#' + formId).val());
    // create new form row from empty form row
    var newFormRow;
    emptyRow.find("input, select, textarea").each(function(){
        newFormRow = updateEmptyFormIDs($(this), totalForms)
    })
    emptyRow.show();
    // insert new form at the end of the last form row
    $(".form-row:last").after(newFormRow)
    // update total form count (to include new row)
    $('#'+ formId).val(totalForms + 1);
    // scroll page to new row
    //new jscolor($('.jscolor').last()[0]);

    $('html, body').animate({
        scrollTop: newFormRow.offset().top - 100
    }, 500, function(){
        // animate background color
        // requires: jQuery Color: https://code.jquery.com/color/jquery.color-2.1.2.min.js
        newFormRow.animate({
            backgroundColor: "#fff"
        }, 1500)
    });

    $('.delete-form').click(function(e) {
        e.preventDefault()
        var count = $(".form-row").length;
        if (count > 1) {
          // form id like #id_form-TOTAL_FORMS
          var formId = "id_ajouter-cours-TOTAL_FORMS"
          // Insert row after last row
          // get starting form count for formset
          var totalForms = parseInt($('#' + formId).val());

          // update total form count (to include new row)
          $('#'+ formId).val(totalForms - 1);
          // scroll page to new row
          $(".form-row:last").remove();
        }
    });
});
