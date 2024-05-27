/* globals enableUploads, bootstrap, Backbone, _, $ */
const FileModel = Backbone.Model.extend({
  urlRoot: "file",
});

const FileView = Backbone.View.extend({
  tagName: "tr",
  className: "hover",
  template: _.template($("#rowTemplate").html()),

  events: function eventsInit() {
    return {
      "click .access": "_access",
      "click .remove": "_remove",
    };
  },

  _remove: function fileRemove(event) {
    event.preventDefault();
    event.stopPropagation();

    this.model.destroy();
    this.remove();
  },

  _access: function fileAccess() {
    if (this.model.get("access") === "public") {
      this.model.set("access", "limited");
    } else if (this.model.get("access") === "private") {
      this.model.set("access", "public");
    } else {
      this.model.set("access", "private");
    }
    this.model.save();
    this.render();
  },

  render: function fileRender() {
    this.$el.html(this.template(this.model.toJSON()));
  },
});

$(document).ready(() => {
  // initialize existing files
  _.each(bootstrap, (file) => {
    const model = new FileModel(file);
    const view = new FileView({
      model: model,
      el: $(`#key_${model.get("key")}`).get(0),
    });
  });
});

const addFile = function (file) {
  console.log(file);
  const model = new FileModel({ ...file });

  const view = new FileView({ model: model });
  $("#files").prepend(view.el);
  view.render();
};

document.addEventListener("DOMContentLoaded", () => {
  enableUploads(addFile);
});
