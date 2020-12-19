function ValidateSize(file) {
    var FileSize = file.files[0].size / 1024 / 1024; // in MiB
    if (FileSize > 4) {
        alert('File size exceeds 4 MB');
       // $(file).val(''); //for clearing with Jquery
    } else {

    }
}