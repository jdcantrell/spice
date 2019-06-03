/* globals enableUploads */
const addItem = ({ key }) => {
  fetch(`html/${key}`).then(response => {
    response.text().then(html => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const log = document.getElementById('log_list');
      const el = doc.body.firstChild;
      el.classList.add('photo-card-enter');
      log.insertBefore(el, log.firstChild)
      setTimeout(() => { el.classList.remove('photo-card-enter') }, 10);
    })
  });
};

const removeItem = (id) => {
  fetch(`/file/${id}`, { method: 'DELETE' }).then(response => {
    const el = document.getElementById(`photo_card_${id}`);
    el.classList.add('photo-card-exit');
    setTimeout(() => { el.remove() }, 200);
  });
};

const setMode = (selectEl, id) => {
  const newAccess = selectEl.value;
  selectEl.previousElementSibling.innerHTML = newAccess;
  fetch(`/file/${id}`, {
    method: 'PUT',
    cache: 'no-cache',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ access: newAccess })

  });
};


document.addEventListener('DOMContentLoaded', function(event) {
  enableUploads(addItem);
});
