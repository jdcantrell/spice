/* globals bootstrap */
var FileModel = Backbone.Model.extend({
  urlRoot: 'file',
  upload: function () {
    var self = this;
    //using XHR directly because jquery does not expose the upload
    //property - works in chrome and FF (IE shouldn't get this code)
    var xhr = new XMLHttpRequest();

    xhr.upload.addEventListener("progress", function (e) {
      if (e.lengthComputable) {
        var percentage = Math.round((e.loaded * 100) / e.total);
        self.set({
          'status': 'uploading',
          'progress': percentage,
          'loaded': e.loaded,
          'total': e.total
        });
      }
    }, false);

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if ((xhr.status >= 200 && xhr.status <= 200) || xhr.status === 304) {
          if (xhr.responseText !== "") {
            var item = $.parseJSON(xhr.responseText);
            self.set(item);
          }
        }
      }
    };

    var data = new FormData();
    data.append('file', self.get('file'));
    data.append('access', self.get('access'));
    data.append('json', true);

    xhr.open("POST", "/file");
    xhr.send(data);
  }
});

var FileView = Backbone.View.extend({
  tagName: 'tr',
  className: 'hover',
  uploadTemplate: _.template($('#uploadTemplate').html()),
  template: _.template($('#rowTemplate').html()),

  events: function () {
    this.listenTo(this.model, 'change:progress', this.render);
    this.listenTo(this.model, 'change:key', this.render);
    return {
      'click .access': '_access',
      'click .remove': '_remove'
    };
  },

  _remove: function () {
    this.model.delete();
    this.remove();
  },

  _access: function () {
    if (this.model.get('access') === 'public') {
      this.model.set('access', 'limited');
    }
    else if (this.model.get('access') === 'private') {
      this.model.set('access', 'public');
    }
    else {
      this.model.set('access', 'private');
    }
    this.model.save();
    this.render();
  },

  render: function () {
    if (this.model.get('key')) {
      this.$el.html(this.template(this.model.toJSON()));
    }
    else {
      this.$el.html(this.uploadTemplate(this.model.toJSON()));
    }
  }
});

$(document).ready(function () {
  var access = 'limited';
  $('#access_controls button').click(function () {
    $el = $(this);
    console.log($el.val());
    access = $el.val();
    $el.parent().children().removeClass('button-active');
    $el.addClass('button-active')
  });
  //file api code
  if (typeof FileReader === "function") {

    //add our dnd listeners
    $('body').bind({
      dragover: function (event) { event.preventDefault(); },
      dragleave: function (event) { event.preventDefault(); },
      drop: function (event) {
        event.preventDefault();

        var originalEvent = event.originalEvent;
        var files = (originalEvent.files || originalEvent.dataTransfer.files);
        for (var i = 0; i < files.length; i += 1) {
          //queue objects to be uploaded
          var file = files[i];
          var model = new FileModel({
            name: file.name,
            access: access,
            progress: 0,
            status: 'queued',
            file: file
          });

          var view = new FileView({model: model});
          $('#files').prepend(view.el);
          view.render();

          model.upload();
        }
      }
    });
  }

  //initialize existing files
  _.each(bootstrap, function (file) {
    var model = new FileModel(file);
    var view = new FileView({
      model: model,
      el: $('#key_' + model.get('key')).get(0)
    });
  });
});
