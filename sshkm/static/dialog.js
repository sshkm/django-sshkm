$(".checkAll").click(function () {
    $(this).closest('form').find(':checkbox').prop('checked', $(this).prop('checked'));
});
