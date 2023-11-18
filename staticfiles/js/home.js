//function for validateform

function validateForm() {
    var input = document.getElementById('n');
    if (input.checkValidity()) {
      document.getElementById('myform').submit();
    } else {
      input.reportValidity();
    }
  }