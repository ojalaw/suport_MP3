function deletePost(postId) {
    fetch("/delete-post", {
      method: "POST",
      body: JSON.stringify({ postId:postId }),
    }).then(response => {
        location.reload(true); 
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
