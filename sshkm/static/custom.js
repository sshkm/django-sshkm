// select all functionality
$(".checkAll").click(function () {
  $(this).closest('form').find(':checkbox').prop('checked', $(this).prop('checked'));
});

function checkboxCheck(action, element, title_confirm, message_confirm, title_noselect, message_noselect) {
  var checkboxs=document.getElementsByName(element);
  var okay=false;

  for(var i=0,l=checkboxs.length;i<l;i++) {
    if(checkboxs[i].checked) {
      okay=true;
      break;
    }
  }

  if(okay) {
    BootstrapDialog.confirm(
      {
        title: title_confirm,
        message: message_confirm,
        btnOKClass: 'btn-default',
        callback: function(result) {
          if(result) {
            action();
          }
        }
      }
    );
  } else {
    BootstrapDialog.alert(
      {
        title: title_noselect,
        message: message_noselect,
        btnOKClass: 'btn-default'
      }
    );
  }
}

