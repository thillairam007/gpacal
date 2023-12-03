
function redirectToHome(url) {
  window.location.href = url; // Redirect to the provided URL
}

  
  $(document).ready(function() {
    $('#deptselect').select2({
      placeholder: 'Search for a department',
      allowClear: true,
      matcher: function(params, data) {
        // If there are no search terms, return all options
        if ($.trim(params.term) === '') {
          return data;
        }
        
        // Match search term against option text
        var text = data.text.toLowerCase();
        var term = params.term.toLowerCase();
        
        if (text.indexOf(term) > -1) {
          return data;
        }
        
        // Match search term against option value
        if (data.id.toLowerCase().indexOf(term) > -1) {
          return data;
        }
        
        return null; // no match
      }
    }).on('select2:open', function() {
      // Add a text input inside the dropdown when opened
      $('.select2-search__field').attr('type', 'text');
    });
  });