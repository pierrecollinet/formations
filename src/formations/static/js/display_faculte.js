  function display_facultes(){
            var universite_id = $('#div_id_etude_user-universite :selected').val();
            $('#div_id_etude_user-faculte').show()
            request_url = '/apprenants/get_faculte/' + universite_id + '/';
            $.ajax({
                  url: request_url,
                  success: function(json){
                    var strResult;
                    $('#div_id_etude_user-faculte').empty();
                    strResult = '<label for="id_etude_user-faculte" class="control-label  requiredField">'+
                      'Faculté<span class="asteriskField">*</span> </label><br>'+
                      '<select name="etude_user-faculte" class="select form-control" required="" id="id_etude_user-faculte">'

                      for(var j = 0; j < json.length; j++){
                            strResult += '<option value="' + parseInt(json[j][0]) + '">' + json[j][1] +'</option>'
                        }
                        strResult += '</select>'
                        console.log(strResult)
                        $('#div_id_etude_user-faculte').append(strResult)
                  }
            })
  }
  $('#div_id_etude_user-faculte').hide()
  if ($('#div_id_etude_user-universite')){
    display_facultes();
  }
  $('#div_id_etude_user-universite').change(function() {
    display_facultes();
  });
