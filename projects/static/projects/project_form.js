$(document).ready(function(){
    $('select[name=organization_owner]').attr('required',true);

    if($('#id_owner_type').val() == 'm') {
        $('#organization_owner').hide();
        $('select[name=organization_owner]').attr('required',false);
    }

    if($('#id_project_type').val() == 'p') {
        $('#git_owner').hide();
        $('#git_name').hide();
    } else {
        $('input[name=git_owner]').attr('required', true);
        $('input[name=git_name]').attr('required', true);
    }

    $('#id_owner_type').change(function() {
        if($(this).val() == 'o') {
            $('#organization_owner').show();
            $('select[name=organization_owner]').attr('required',true);
        } else {
            $('#organization_owner').hide();
            $('select[name=organization_owner]').attr('required',false);
        }
    });

    $('#id_project_type').change(function() {
        if($(this).val() == 'g') {
            $('#git_owner').show();
            $('#git_name').show();
            $('input[name=git_owner]').attr('required', true);
            $('input[name=git_name]').attr('required', true);
        } else {
            $('#git_owner').hide();
            $('#git_name').hide();
            $('input[name=git_owner]').val('');
            $('input[name=git_name]').val('');
            $('input[name=git_owner]').attr('required', false);
            $('input[name=git_name]').attr('required', false);
        }
    });
});