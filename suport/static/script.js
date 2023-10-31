// Delete post function
function deletePost(postId) {

  const post = document.getElementById(`post-${postId}`);

  post.style.display = 'none';

  return fetch("/delete-post", {
    method: "POST",
    body: JSON.stringify({ postId: postId})
  })
  .then(response => {
    if(!response.ok) {
      post.style.display = 'block'; 
    }
    return response;
  })
}

// Edit post form reveal
function showEditPostForm(postId) {
  const form = document.getElementById(`edit-post-form-${postId}`);
  form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

// Save edit post
function saveEditedPost(postId) {
  const form = document.getElementById(`edit-post-form-${postId}`);
  const newText = form.querySelector('input[name="text"]').value;

  fetch('/edit-post', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          postId: postId,
          text: newText
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.error) {
          alert(data.error);
      } else {
          alert(data.message);
          location.reload();
      }
  });
}

// Toggle comment form
function toggleCommentForm(postId) {
const form = document.getElementById(`comment-form-${postId}`);
form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

// Delete comment function
function deleteComment(commentId) {
  fetch(`/delete-comment/${commentId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert(data.message);
      const commentElement = document.getElementById(`comment-${commentId}`);
      if (commentElement) {
        commentElement.remove();
      }
    } else {
      alert(data.message);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

// Toggle visibility for edit forms on 'my profile'
document.addEventListener("DOMContentLoaded", function () {
  const editButtons = document.querySelectorAll(".profile-button");

  editButtons.forEach((button) => {
      button.addEventListener("click", function () {
          const field = this.getAttribute("data-field");
          const correspondingField = document.querySelector(`form[data-field="${field}"]`);

          if (correspondingField.style.display === "none" || correspondingField.style.display === "") {
              correspondingField.style.display = "block";
          } else {
              correspondingField.style.display = "none";
          }
      });
  });
});

// Utility functions

function timeSince(date) {

  const seconds = Math.floor((new Date() - date) / 1000);

  let interval = seconds / 31536000;

  if (interval > 1) {
    return Math.floor(interval) + " years ago";
  }
  interval = seconds / 2592000;
  if (interval > 1) {
    return Math.floor(interval) + " months ago";
  }
  interval = seconds / 86400;
  if (interval > 1) {
    return Math.floor(interval) + " days ago";
  }
  interval = seconds / 3600;
  if (interval > 1) {
    return Math.floor(interval) + " hours ago";
  }
  interval = seconds / 60;
  if (interval > 1) {
    return Math.floor(interval) + " minutes ago";
  }
  return Math.floor(seconds) + " seconds ago";
} 

document.addEventListener("DOMContentLoaded", function() {

  let postEls = document.querySelectorAll('.post-time');

  postEls.forEach(el => {
    let timestamp = new Date(el.dataset.postdate); 
    el.innerText = timeSince(timestamp);
  })

  let commentEls = document.querySelectorAll('.comment-time');

  commentEls.forEach(el => {
    let timestamp = new Date(el.dataset.commentdate);
    el.innerText = timeSince(timestamp); 
  })

});



