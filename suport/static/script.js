function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/home";
    });
  }

  function showEditNoteForm(noteId) {
    // Toggle the display of the edit form
    const form = document.getElementById(`edit-note-form-${noteId}`);
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function saveEditedNote(noteId) {
    const form = document.getElementById(`edit-note-form-${noteId}`);
    const newText = form.querySelector('input[name="text"]').value;

    fetch('/edit-note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            noteId: noteId,
            text: newText
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
            location.reload();  // Reload the page to reflect the changes
        }
    });
}
