/*
 * Auto update uuid input fields for forms which support it.
 */
$("[data-uuid][data-target]").click(function() {
    var clicked = $(this);
    var uuid = clicked.data('uuid');
    var target = $(clicked.data('target'));
    target.find('input[name="uuid"]').val(uuid);
});
