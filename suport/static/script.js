// Password reqwuirements
function showPasswordRequirements() {
  document.getElementById("password-requirements").style.display = "block";
}

// Delete post function
function deletePost(postId) {

  const post = document.getElementById(`post-${postId}`);

  post.style.display = 'none';

  return fetch("/delete-post", {
    method: "POST",
    body: JSON.stringify({ postId: postId })
  })
  .then(response => {
    if(!response.ok) {
      post.style.display = 'block'; 
    } else {
      hideConfirm();
    }
    window.location.reload();
  });
}

// Delete Modal
function showConfirmDelete(postId) {
  document.getElementById("confirm-delete-button").setAttribute("onclick", `deletePost('${postId}')`);
  var myModal = new bootstrap.Modal(document.getElementById('confirm-modal'));
  myModal.show();
}

function hideConfirm() {
  var myModal = bootstrap.Modal.getInstance(document.getElementById('confirm-modal'));
  myModal.hide();
}

// Function to reveal the Edit Post form.
function showEditPostForm(postId) {
  const form = document.getElementById(`edit-post-form-${postId}`);
  form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

// Function to hide the Edit Post form when the "Cancel" button is clicked.
function hideEditPostForm(postId) {
  const form = document.getElementById(`edit-post-form-${postId}`);
  form.style.display = 'none';
}

// edit post

function saveEditedPost(postId) {
  const form = document.getElementById(`edit-post-form-${postId}`);
  const newText = form.querySelector('textarea[name="text"]').value;

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
  .then(() => {
      location.reload();
  });
}

// Toggle comment form
function toggleCommentForm(postId) {
const form = document.getElementById(`comment-form-${postId}`);
form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

// Delete Comment function
function deleteComment(commentId) {
  const comment = document.getElementById(`comment-${commentId}`);

  comment.style.display = 'none';

  return fetch(`/delete-comment/${commentId}`, {
    method: "POST"
  })
  .then(response => {
    if(!response.ok) {
      comment.style.display = 'block'; 
    } else {
      hideCommentConfirm();
      window.location.reload();
    }
    return response;
  });
}

// Show Delete Comment Modal
function showCommentConfirmDelete(commentId) {
  document.getElementById("confirm-comment-delete-button").setAttribute("onclick", `deleteComment('${commentId}')`);
  var myModal = new bootstrap.Modal(document.getElementById('confirm-comment-delete-modal'));
  myModal.show();
}

// Hide Delete Comment Modal
function hideCommentConfirm() {
  var myModal = bootstrap.Modal.getInstance(document.getElementById('confirm-comment-delete-modal'));
  myModal.hide();
}

// Toggle visibility for edit forms on 'my profile'
document.querySelectorAll('.profile-button').forEach(function (button) {
  button.addEventListener('click', function () {
    const field = this.getAttribute('data-field');
    const editForm = document.querySelector(`.edit-field[data-field="${field}"]`);
    const cancelButton = editForm.querySelector('.cancel-button');

    if (editForm.style.display === 'none' || editForm.style.display === '') {
      editForm.style.display = 'block';
      cancelButton.style.display = 'inline-block';
      this.style.display = 'none';
    } else {
      editForm.style.display = 'none';
      cancelButton.style.display = 'none';
      this.style.display = 'inline-block';
    }
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
  });

  let commentEls = document.querySelectorAll('.comment-time');

  commentEls.forEach(el => {
    let timestamp = new Date(el.dataset.commentdate);
    el.innerText = timeSince(timestamp); 
  });

});