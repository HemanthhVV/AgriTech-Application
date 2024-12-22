function openImageViewer(imageUrl) {
    const modal = document.querySelector('#imageViewer');
    const modalImage = document.querySelector('#modalImage');
    modalImage.src = imageUrl; // Set the clicked image's URL
    modal.classList.remove('hidden'); // Show the modal
}

function closeImageViewer() {
    const modal = document.getElementById('imageViewer');
    modal.classList.add('hidden'); // Hide the modal
}
function openDeleteModal(uuid) {
    const modal = document.getElementById('deleteModal');
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.action = `/delete/${uuid}`; // Update the action URL dynamically
    modal.classList.remove('hidden'); // Show the modal
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.add('hidden'); // Hide the modal
}