/* exported enableUploads */
const enableUploads = (onUploadComplete = () => {}) => {
  const uploadFile = (fileData, access, onProgress) => {
    const uploadPromise = new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();

      xhr.upload.addEventListener(
        'progress',
        e => {
          if (e.lengthComputable) {
            const percentage = Math.round((e.loaded * 100) / e.total);
            onProgress(percentage, e.loaded, e.total);
          }
        },
        false
      );

      xhr.onreadystatechange = function readyStateChange() {
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

      const data = new FormData();
      data.append('file', fileData);
      data.append('access', access);
      data.append('json', true);

      xhr.open('POST', '/file/');
      xhr.send(data);
    });

    return uploadPromise;
  };

  const displayProgress = (name, totalFiles, currentFile, percent) => {
    const el = document.getElementById('status');

    el.style.backgroundSize = `${percent}%`;
    if (percent < 100) {
      if (totalFiles > 1) {
        el.innerHTML = `[${currentFile}/${totalFiles}] Uploading ${name} ${percent}%`;
      } else {
        el.innerHTML = `Uploading ${name} ${percent}%`;
      }
    }
    if (totalFiles > 1) {
      el.innerHTML = `[${currentFile}/${totalFiles}] Processing ${name} ${percent}%`;
    } else {
      el.innerHTML = `Processing ${name} ${percent}%`;
    }
  };

  const doUpload = (file, access, totalFiles, currentFile) =>
    uploadFile(file, access, (percent, uploaded, totalSize) => {
      displayProgress(
        file.name,
        totalFiles,
        currentFile,
        percent,
        uploaded,
        totalSize
      );
    });

  const resetProgress = () => {
    const el = document.getElementById('status');
    el.innerHTML = '&nbsp;';
    el.style.backgroundSize = `0%`;
    el.classList.remove('progress-hide');
  };

  let doneTimeout;
  const uploadFiles = files => {
    // get current selected access level
    const access = document
      .getElementById('access_controls')
      .querySelector('.primary').value;

    let promise;

    window.clearTimeout(doneTimeout);
    resetProgress();
    for (let i = 0; i < files.length; i += 1) {
      const file = files[i];
      if (promise) {
        promise = promise.then(() => {
          return doUpload(file, access, files.length, i + 1).then(
            onUploadComplete
          );
        });
      } else {
        promise = doUpload(file, access, files.length, i + 1).then(
          onUploadComplete
        );
      }
    }

    return promise.then(() => {
      const el = document.getElementById('status');
      el.classList.add('progress-hide');
      el.innerHTML = 'Done!';
      doneTimeout = setTimeout(resetProgress, 5000);
    });
  };

  document.addEventListener(
    'drop',
    event => {
      event.preventDefault();
      const files = event.files || event.dataTransfer.files;
      uploadFiles(files);
    },
    false
  );

  document.addEventListener(
    'dragover',
    event => {
      event.preventDefault();
    },
    false
  );

  document.addEventListener(
    'dragleave',
    event => {
      event.preventDefault();
    },
    false
  );

  // Hook up button group selector
  document
    .getElementById('access_controls')
    .querySelectorAll('button')
    .forEach(el => {
      el.addEventListener('click', () => {
        document
          .getElementById('access_controls')
          .querySelector('.primary')
          .classList.remove('primary');
        el.classList.add('primary');
      });
    });

  // Add paste catcher
  const pasteEl = document.getElementById('paste_box');
  pasteEl.addEventListener('paste', ({ clipboardData }) => {
    const { items } = clipboardData;
    const files = [];
    if (items) {
      // Loop through all items, looking for any kind of image
      for (let i = 0; i < items.length; i += 1) {
        if (items[i].type.indexOf('image') !== -1) {
          // TODO: test in chrome
          const pasteFile = items[i].getAsFile();
          if (pasteFile.name.startsWith('image.')) {
            const now = new Date();
            const name = `Image ${now.toDateString()} ${now.toLocaleTimeString()}.`;
            files.push(
              new File([pasteFile], pasteFile.name.replace('image.', name), {
                type: pasteFile.type,
              })
            );
          } else {
            files.push(pasteFile);
          }
        }
      }
      if (files.length) {
        uploadFiles(files);
      }
    } else {
      console.log('No clipboard data found for pasting');
    }
    pasteEl.innerHTML = '';
  });

  document.body.addEventListener('click', () => pasteEl.focus());
  pasteEl.focus();
};
