const enableUploads = () => {
  const uploadFile = (fileData, access, onProgress) => {
    const uploadPromise = new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();

      xhr.upload.addEventListener(
        'progress',
        function(e) {
          if (e.lengthComputable) {
            var percentage = Math.round((e.loaded * 100) / e.total);
            onProgress(percentage, e.loaded, e.total);
          }
        },
        false
      );

      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
          if ((xhr.status >= 200 && xhr.status <= 200) || xhr.status === 304) {
            if (xhr.responseText !== '') {
              resolve(JSON.parse(xhr.responseText));
            }
          } else {
            reject();
          }
        }
      };

      var data = new FormData();
      data.append('file', fileData);
      data.append('access', access);
      data.append('json', true);

      xhr.open('POST', '/file');
      xhr.send(data);
    });

    return uploadPromise;
  };

  const displayProgress = (
    name,
    totalFiles,
    currentFile,
    percent,
    loaded,
    total
  ) => {
    const el = document.getElementById('status');
    el.style.backgroundSize = `${percent}%`;
    if (totalFiles > 1) {
      el.innerHTML = `[${currentFile}/${totalFiles}] Uploading ${name} ${percent}%`;
    } else {
      el.innerHTML = `Uploading ${name} ${percent}%`;
    }
  };

  const doUpload = (file, access, totalFiles, currentFile) => {
    return uploadFile(file, access, (percent, uploaded, totalSize) => {
      displayProgress(
        file.name,
        totalFiles,
        currentFile,
        percent,
        uploaded,
        totalSize
      );
    });
  };

  const resetProgress = () => {
    const el = document.getElementById('status');
    el.innerHTML = '&nbsp;';
    el.style.backgroundSize = `0%`;
    el.classList.remove('progress-hide');
  };

  let doneTimeout;
  document.addEventListener(
    'drop',
    function(event) {
      console.log('drop');
      event.preventDefault();
      const files = event.files || event.dataTransfer.files;

      // get current selected access level
      const access = document
        .getElementById('access_controls')
        .querySelector('.primary').value;
      console.log('found some files');

      let promise;

      window.clearTimeout(doneTimeout);
      resetProgress();
      for (let i = 0; i < files.length; i += 1) {
        const file = files[i];
        if (promise) {
          promise = promise.then(() => {
            return doUpload(file, access, files.length, i + 1);
          });
        } else {
          promise = doUpload(file, access, files.length, i + 1);
        }
      }

      promise.then(() => {
        const el = document.getElementById('status');
        el.classList.add('progress-hide');
        doneTimeout = setTimeout(resetProgress, 4501);
      });
    },
    false
  );

  document.addEventListener(
    'dragover',
    function(event) {
      event.preventDefault();
    },
    false
  );

  document.addEventListener(
    'dragleave',
    function(event) {
      event.preventDefault();
    },
    false
  );

  // Hook up button group selector
  document
    .getElementById('access_controls')
    .querySelectorAll('button')
    .forEach(el => {
      el.addEventListener('click', event => {
        document
          .getElementById('access_controls')
          .querySelector('.primary')
          .classList.remove('primary');
        el.classList.add('primary');
      });
    });
};

document.addEventListener('DOMContentLoaded', function(event) {
  enableUploads();
});
