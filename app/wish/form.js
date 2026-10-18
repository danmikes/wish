document.addEventListener('DOMContentLoaded', function() {
  function getDomain(url) {
    try {
      const urlParts = new URL(url);
      let hostname = urlParts.hostname.replace('www.', '');
      const lastDotIndex = hostname.lastIndexOf('.');
      return lastDotIndex !== -1 ? hostname.substring(0, lastDotIndex) : hostname;
    } catch (e) {
      return '';
    }
  }

  const descriptionInput = document.getElementById('description-input');
  const descriptionPreview = document.getElementById('description-preview');
  const urlInput = document.getElementById('url-input');
  const urlPreview = document.getElementById('url-preview');
  const fileName = document.getElementById('file-name');
  const imageInput = document.getElementById('image-input');
  const imagePreview = document.getElementById('image-preview');
  const addBtn = document.getElementById('add-image-btn');
  const deleteBtn = document.getElementById('delete-image-btn');

  let currentImage = "{{ wish.image }}";
  let addedImages = [];
  let markedForDeletion = [];

  descriptionPreview.innerText = document.getElementById('description-input').value;
  const initialUrl = urlInput.value;
  urlPreview.href = initialUrl;
  urlPreview.innerText = getDomain(initialUrl);

  descriptionInput.addEventListener('input', function() {
    descriptionPreview.innerText = this.value;
  });

  urlInput.addEventListener('input', function() {
    const url = this.value;
    urlPreview.href = url;
    urlPreview.innerText = getDomain(url);
  });

  addBtn.addEventListener('click', function() {
    imageInput.click()
  });

  imageInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function(event) {
        imagePreview.src = event.target.result;
        fileName.value = file.name;
        deleteBtn.removeAttribute('disabled');

        addedImages.push({
          name: file.name,
          dataUrl: event.target.result,
        });

        markedForDeletion = markedForDeletion.filter(img => img.name != file.name);
      };
      reader.readAsDataURL(file);
    } else {
      console.log('No file selected');
    }
  });

  deleteBtn.addEventListener('click', function() {
    if (confirm('Delete image?')) {
      if (currentImage) {
        currentImage = null;
        imagePreview.src = '';
        fileName.value = '';
        deleteBtn.setAttribute('disabled', true);

        document.getElementById('marked_for_deletion').value = 'true';

        imageInput.value = '';

        const index = addedImages.findIndex(img => img.name === fileName.value);
        if (index > -1) {
          addedImages.splice(index, 1);
        }
      }
    }
  });
});
