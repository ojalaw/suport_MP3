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
