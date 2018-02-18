tinymce.init({
    selector: 'textarea',
    height: '15%',
    menubar: false,
    statusbar: false,
    plugins: [
      'advlist autolink lists link image charmap print preview anchor textcolor',
      'searchreplace visualblocks code fullscreen emoticons',
      'insertdatetime media table paste code help wordcount'
    ],
    toolbar: 'insertdatetime | undo redo | bold italic underline | forecolor backcolor | emoticons | bullist numlist | code link | removeformat | help',
    content_css: [
      '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
      '//www.tinymce.com/css/codepen.min.css']
});