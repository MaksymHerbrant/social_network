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
// function showDialog() {
//   $('#openDialogButtonsearch').click(function() {
//     $('#dialogsearch').show();
//     $('#overlay').show();
//   });
// }

// function closeDialogue() {
//   $('#closeDialogButton').click(function() {
//     $('#myDialog').hide();
//     $('#overlay').hide();
//   });
// }

    
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
  
    function addLike() {
      $('.like').click(function() {
        let btn = $(this);
        let postId = btn.data('post-id');
        let likeAmount = btn.next('.like-amount');
    
        $.ajax(btn.data('url'), {
          'type': 'POST',
          'async': true,
          'dataType': 'json',
          'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'like': 1
          },
          'success': function(data) {
        if (data['is_like']) {
        btn.find('img').attr('src', '/static/img/base/like.png');
        likeAmount.text(data['like_count']);
        } else {
        btn.find('img').attr('src', '/static/img/base/dislike.png');
        likeAmount.text(data['like_count']);
        }
          }
        });
      });
    }
    
    $(document).ready(function() {
      addLike();
    
      $('.like').each(function() {
        let btn = $(this);
        let postId = btn.data('post-id');
        let likeAmount = btn.next('.like-amount');
    
        $.ajax(btn.data('url'), {
          'type': 'POST',
          'async': true,
          'dataType': 'json',
          'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'is_like': 1
          },
          'success': function(data) {
            if (data['is_like']) {
                 btn.find('img').attr('src', '/static/img/base/like.png');
                } else {
                 btn.find('img').attr('src', '/static/img/base/dislike.png');
                }
            likeAmount.text(data['like_amount']);
          }
        });
      });
    });   

    $(document).ready(function() {
      // Функція для додавання коментарів
      function addComment() {
        console.log('addComment() function called.');
        $('.comment-form').submit(function(event) {
          event.preventDefault(); // Зупинити стандартну відправку форми
    
          let form = $(this);
          let url = form.attr('action'); // Отримати URL з атрибуту action форми
          let postId = form.data('post-id'); // Отримати ідентифікатор поста з атрибуту data-post-id форми
    
          let commentBody = form.find('input[name="text"]').val().trim();
    
          // Перевірка, щоб не надсилати порожні коментарі
          if (commentBody === '') {
            return;
          }
    
          // Отримати токен CSRF з метатега в шаблоні
          let csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    
          // Створення об'єкту даних для надсилання
          let data = {
            'csrfmiddlewaretoken': csrfToken,
            'text': commentBody
          };
    
          // Надсилання запиту AJAX для додавання коментаря
          $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            data: data,
            success: function(response) {
              // Очистити поле введення коментаря
              form.find('input[name="text"]').val('');
    
              // Оновити відображення коментарів
              let commentHtml = '<h4 id="' + response.id + '" class="comment">' +
                response.username + '<br>' + response.body + '</h4>';
              let commentsContainer = $('#comments-' + postId);
              let commentElement = $(commentHtml);
    
              let deleteButton = $('<button type= "submit" class="delete-button"><img src="/static/img/base/trash.png" width="25"></button>');
              deleteButton.click(function() {
                deleteComment(response.id);
              });
    
              commentElement.append('<br>');
              commentElement.append(deleteButton);
    
              commentsContainer.append(commentElement);
            },
            error: function(xhr, textStatus, errorThrown) {
              console.log(xhr.responseText);
            }
          });
        });
      }
    
      // Виклик функції для додавання коментарів
      addComment();
    
      // Функція для видалення коментарів
      function deleteComment(commentId) {
        let url = '/delete_comment/' + commentId + '/';
    
        $.ajax({
          url: url,
          type: 'POST',
          dataType: 'json',
          data: {
            'comment_id': commentId,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
          },
          success: function(response) {
            // Видалити коментар зі сторінки
            $('#' + commentId).remove();
          },
          error: function(xhr, textStatus, errorThrown) {
            console.log(xhr.responseText);
          }
        });
      }
    });
    