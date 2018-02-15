$('document').ready(function() {
        $('[data-tooltip="tooltip"]').tooltip();

        $('button[name=reply-btn]').click(function () {
            var comment_id = $(this).parents('tr').find('td[name=comment_id]').attr('id');
            tinymce.get('id_text').setContent('');
            $('#resource_id').val(comment_id);
        });
        $('button[name=edit-btn]').click(function () {
            var comment_id = $(this).parents('tr').find('td[name=comment_id]').attr('id');
            var comment_text = $(this).parents('tr').find('td[name=comment_content] p[name=comment_text]').next().html();
            tinymce.get('id_text').setContent(comment_text);
            $('#update_comment_id').val(comment_id);
       });
        $('button[name=toggle-btn]').click(function () {
            var comment_id = $(this).parents('tr').find('td[name=comment_id]').attr('id');
            $('tr[name=replies' + comment_id + ']').toggle();
       });
});