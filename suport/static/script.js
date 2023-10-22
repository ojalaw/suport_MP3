function deleteReview(reviewId) {
    fetch("/delete-review", {
      method: "POST",
      body: JSON.stringify({ reviewId: reviewId }),
    }).then(response => {
        showConfirmMessage("Rview deleted!"); 
      })
    
    }

  function showEditReviewForm(reviewId) {
    const form = document.getElementById(`edit-review-form-${reviewId}`);
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function saveEditedReview(reviewId) {
    const form = document.getElementById(`edit-review-form-${reviewId}`);
    const newText = form.querySelector('input[name="text"]').value;

    fetch('/edit-review', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            reviewId: reviewId,
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
