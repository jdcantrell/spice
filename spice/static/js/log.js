const addItem = ({ key }) => {
  fetch(`html/${key}`).then(response => {
    console.log('got html', response);
  });
};
document.addEventListener('DOMContentLoaded', function(event) {
  enableUploads(addItem);
});
