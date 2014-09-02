/* exported layout_tiles */
function set_image_height(els, targetHeight, maxWidth) {
  _.each(els, function (el) {
    var $el = $(el);
    if (el.naturalHeight) {
      var css = {visiblity: 'visible'};
      var padding, targetWidth;
      if (els.length === 1) {
        targetWidth = maxWidth;
      }
      else {
        targetWidth = targetHeight / el.naturalHeight * el.naturalWidth;
        targetWidth = targetWidth > maxWidth ? maxWidth : targetWidth;
      }

      if (targetWidth > el.naturalWidth) {
        padding = (targetWidth - el.naturalWidth - 2) / 2;
        css.paddingLeft = padding + 'px';
        css.paddingRight = padding + 'px';
        $el.addClass('image-frame');
      }
      else {
        css.width = targetWidth;
      }

      if (targetHeight > el.naturalHeight) {
        padding = (targetHeight - el.naturalHeight - 2) / 2;
        css.paddingTop = padding + 'px';
        css.paddingBottom = padding + 'px';
        $el.addClass('image-frame');
      }
      else {
        css.height = targetHeight;
      }

      $el.css(css);
    }
    else {
      var width = targetHeight / $el.attr('natural-height') * $el.attr('natural-width');
      if (width > 656) {
        width = 656;
      }
      $el.removeClass('image-frame');
      $el.css({
        width: width,
        height: targetHeight,
        visibility: 'visibile'
      });

    }
  });
}

function layout_tiles($els, targetHeight, rowWidth, marginTotal) {
  var currentWidth = 0;

  var rowImgs = [];


  $els.each(function (idx, el) {
    var scaledWidth;
    if (el.naturalHeight) {
      //We have an image
      scaledWidth = (targetHeight / el.naturalHeight * el.naturalWidth);
    }
    else {
      //We have some other markup
      scaledWidth = (targetHeight / $(el).attr('natural-height') * $(el).attr('natural-width'));
    }
    if (currentWidth + scaledWidth < rowWidth) {
      currentWidth += scaledWidth;
      rowImgs.push(el);
    }
    else {
      var width = rowImgs.length * marginTotal + currentWidth;
      var scale_up = (rowWidth - width < (width + scaledWidth) - rowWidth);
      if (!scale_up) {
        //scale images down by adding the next image to the row
        rowImgs.push(el);
        currentWidth += scaledWidth;
        width = rowImgs.length * marginTotal + currentWidth;
      }
      var rowHeight = rowWidth / (width) * targetHeight;
      //update heights
      set_image_height(rowImgs, rowHeight, rowWidth - marginTotal);
      rowImgs = [];
      currentWidth = 0;
      if (scale_up) {
        rowImgs.push(el);
        currentWidth = scaledWidth;
      }
    }
  });


  if (rowImgs.length) {
    set_image_height(rowImgs, targetHeight);
  }
}

