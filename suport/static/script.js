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
    
  function showEditPostForm(postId) {
    const form = document.getElementById(`edit-post-form-${postId}`);
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

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