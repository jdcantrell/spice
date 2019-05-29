/* globals enableUploads, bootstrap, Backbone, _, $ */
const FileModel = Backbone.Model.extend({
  urlRoot: 'file',
});

const FileView = Backbone.View.extend({
  tagName: 'tr',
  className: 'hover',
  template: _.template($('#rowTemplate').html()),

  events: function eventsInit() {
    return {
      'click .access': '_access',
      'click .remove': '_remove',
    };
  },

  _remove: function fileRemove(event) {
    event.preventDefault();
    event.stopPropagation();

    this.model.destroy();
    this.remove();
  },

  _access: function fileAccess() {
    if (this.model.get('access') === 'public') {
      this.model.set('access', 'limited');
    } else if (this.model.get('access') === 'private') {
      this.model.set('access', 'public');
    } else {
      this.model.set('access', 'private');
    }
    this.model.save();
    this.render();
  },

  render: function fileRender() {
    console.log('render', this.model.toJSON());
    this.$el.html(this.template(this.model.toJSON()));
  },
});

$(document).ready(() => {
  // initialize existing files
  _.each(bootstrap, file => {
    const model = new FileModel(file);
    const view = new FileView({
      model: model,
      el: $(`#key_${model.get('key')}`).get(0),
    });
  });
});

const addFile = function(file) {
  console.log(file);
  const model = new FileModel({ ...file });

  const view = new FileView({ model: model });
  $('#files').prepend(view.el);
  view.render();
};

// const removeItem = (id) => {
//   fetch(`/file/${id}`, { method: 'DELETE' }).then(response => {
//     const el = document.getElementById(`photo_card_${id}`);
//     el.classList.add('photo-card-exit');
//     setTimeout(() => { el.remove() }, 200);
//   });
// };
//
// const setMode = (selectEl, id) => {
//   const newAccess = selectEl.value;
//   selectEl.previousElementSibling.innerHTML = newAccess;
//   fetch(`/file/${id}`, {
//     method: 'PUT',
//     cache: 'no-cache',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({ access: newAccess })
//
//   });
// };

document.addEventListener('DOMContentLoaded', () => {
  enableUploads(addFile);
});
