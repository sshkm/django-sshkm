// select all functionality
$(".checkAll").click(function () {
  $(this).closest('form').find(':checkbox').prop('checked', $(this).prop('checked'));
});


// dialogs
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


// two-side multiselect
$("#btnLeft").click(function () {
  var selectedItem = $("#rightValues option:selected");
  $("#leftValues").append(selectedItem);
});

$("#btnRight").click(function () {
  var selectedItem = $("#leftValues option:selected");
  $("#rightValues").append(selectedItem);
});

function selectAll(box) { 
  selectBox = document.getElementById(box);

  for (var i = 0; i < selectBox.options.length; i++) { 
    selectBox.options[i].selected = true; 
  } 
}


// DataTable
$(document).ready(function(){
  var dataTable = $('.DataTable').DataTable({
    paging: false,
    info: false
  });

  $("#searchbox").on("keyup search input paste cut", function() {
    dataTable.search(this.value).draw();
  });
});

/*
var oTable;
$(document).ready(function(){
  oTable = $(".DataTablePermissions").dataTable({
    info: false,
    "pageLength": 50
  });

  function refreshCurrentPage() {
    var table = $('.DataTablePermissions').DataTable();
    var info = table.page.info();
    $(".tableInfo").text((info.page+1)+' of '+info.pages);
  }

  $(".paginate_left").click(function(){
    oTable.fnPageChange( 'previous' );
    refreshCurrentPage();
  });

  $(".paginate_right").click(function(){
    oTable.fnPageChange( 'next' );
    refreshCurrentPage();
  });

  $(oTable.on('search.dt', function(){
    refreshCurrentPage();
  }));

  $(oTable.off('search.dt', function(){
    refreshCurrentPage();
  }));

  refreshCurrentPage();
});
*/
