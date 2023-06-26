function showDialog() {
    $('#addchat').click(function() {
      $('#myDialog').show();
      $('#overlay').show();
    });
  }
  
  function closeDialogue() {
    $('#closeDialogButton').click(function() {
      $('#myDialog').hide();
      $('#overlay').hide();
    });
  }
  $(document).ready(function(){
    showDialog();
    closeDialogue();
     
  });