/* globals bootstrap, File */
var FileModel = Backbone.Model.extend({
  urlRoot: "file",
  upload: function () {
    var self = this;
    //using XHR directly because jquery does not expose the upload
    //property - works in chrome and FF (IE shouldn't get this code)
    var xhr = new XMLHttpRequest();

    xhr.upload.addEventListener(
      "progress",
      function (e) {
        if (e.lengthComputable) {
          var percentage = Math.round((e.loaded * 100) / e.total);
          self.set({
            status: "uploading",
            progress: percentage,
            loaded: e.loaded,
            total: e.total,
          });
        }
      },
      false,
    );

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
    data.append("file", self.get("file"));
    data.append("access", self.get("access"));
    data.append("json", true);

    xhr.open("POST", this.url());
    xhr.send(data);
  },
});

var FileView = Backbone.View.extend({
  tagName: "tr",
  className: "hover",
  uploadTemplate: _.template($("#uploadTemplate").html()),
  template: _.template($("#rowTemplate").html()),

  events: function () {
    this.listenTo(this.model, "change:progress", this.render);
    this.listenTo(this.model, "change:key", this.render);
    return {
      "click .access": "_access",
      "click .remove": "_remove",
    };
  },

  _remove: function (event) {
    event.preventDefault();
    event.stopPropagation();

    this.model.destroy();
    this.remove();
  },

  _access: function () {
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

  render: function () {
    if (this.model.get("key")) {
      this.$el.html(this.template(this.model.toJSON()));
    } else {
      this.$el.html(this.uploadTemplate(this.model.toJSON()));
    }
  },
});

$(document).ready(function () {
  var access = "limited";
  $("#access_controls button").click(function () {
    var $el = $(this);
    access = $el.val();
    $el.parent().children().addClass("button-lowlight");
    $el.removeClass("button-lowlight");
  });
  //file api code
  if (typeof FileReader === "function") {
    var checkInput = function () {
      var pasteCatcher = $("#paste_box");
      // Store the pasted content in a variable
      var child = pasteCatcher.children().get(0);

      // Clear the inner html to make sure we're always
      // getting the latest inserted content
      pasteCatcher.html("");

      if (child) {
        // If the user pastes an image, the src attribute
        // will represent the image as a base64 encoded string.
        if (child.tagName === "IMG") {
          createImage(child.src);
        }
      }
    };

    var getFileName = function (type) {
      var fileTypes = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/gif": "gif",
      };
      return "Image " + new Date() + "." + fileTypes[type];
    };

    /* Creates a new image from a given source */
    var createImage = function (dataURI) {
      var binary = atob(dataURI.split(",")[1]);
      var mimeType = dataURI.split(",")[0].split(":")[1].split(";")[0];
      var array = [];
      for (var i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
      }

      var blob = new Blob([new Uint8Array(array)], { type: mimeType });
      var file = new File([blob], getFileName(mimeType));
      addFile(file);
    };

    var addFile = function (file) {
      var model = new FileModel({
        name: file.name,
        access: access,
        progress: 0,
        status: "queued",
        file: file,
      });

      var view = new FileView({ model: model });
      $("#files").prepend(view.el);
      $("#empty").remove();
      view.render();

      model.upload();
    };

    $("#paste_box").bind("paste", function (event) {
      var items = event.originalEvent.clipboardData.items;
      if (items) {
        // Loop through all items, looking for any kind of image
        for (var i = 0; i < items.length; i++) {
          if (items[i].type.indexOf("image") !== -1) {
            // TODO: test in chrome
            var blob = items[i].getAsFile();
            addFile(blob);
          }
        }
      } else {
        // If we can't handle clipboard data directly (Firefox),
        // we need to read what was pasted from the contenteditable element
        // This is a cheap trick to make sure we read the data
        // AFTER it has been inserted.
        $(this).html("");
        setTimeout(checkInput, 1);
      }
    });

    $("body").bind({
      click: function () {
        $("#paste_box").focus();
      },
      dragover: function (event) {
        event.preventDefault();
      },
      dragleave: function (event) {
        event.preventDefault();
      },
      drop: function (event) {
        event.preventDefault();

        var originalEvent = event.originalEvent;
        var files = originalEvent.files || originalEvent.dataTransfer.files;
        for (var i = 0; i < files.length; i += 1) {
          //queue objects to be uploaded
          var file = files[i];
          addFile(file);
        }
      },
    });

    //focus on paste catcher
    $("#paste_box").focus();
  }

  //initialize existing files
  _.each(bootstrap, function (file) {
    var model = new FileModel(file);
    var view = new FileView({
      model: model,
      el: $("#key_" + model.get("key")).get(0),
    });
  });
});
