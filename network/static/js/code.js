function showDialog() {
  $('#openDialogButton').click(function() {
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

    
document.querySelectorAll('.like-button').forEach(function(button) {
  button.addEventListener('click', function(event) {
      event.preventDefault(); // Зупиняє перехід за посиланням
      
      var postId = this.getAttribute('data-post-id');

      // Створення AJAX-запиту
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/like/', true);
      xhr.setRequestHeader('Content-Type', 'application/json');

      // Відправка даних на сервер
      var data = JSON.stringify({ postId: postId });
      xhr.send(data);

      // Обробка відповіді від сервера
      xhr.onreadystatechange = function() {
          if (xhr.readyState === 4 && xhr.status === 200) {
              var response = JSON.parse(xhr.responseText);
              // Виклик функції для оновлення відображення лайків на сторінці
              updateLikes(postId, response.likeAmount, response.isLike);
          }
      };
  });
});

function updateLikes(postId, likeAmount, isLike) {
  var likeAmountElement = document.getElementById('like-amount-' + postId);
  var likeButtonElement = document.getElementById('like-button-' + postId);

  if (isLike) {
      likeButtonElement.classList.add('liked');
  } else {
      likeButtonElement.classList.remove('liked');
  }

  likeAmountElement.textContent = likeAmount;
}




    // Виклик функцій
    $(document).ready(function(){
      showDialog();
      closeDialogue();
       
    });
  
   