In progress:
* public, shared, private - need to add list interactions
* tweak link colors
* header row on files list
* Fix queued to say uploading when upload begins

Todo:
* Add remove endpoint
* Create handlers - markdown?
* note field/custom key?

* deploy script (how to not overwrite settings.cfg)
  deploy update
  git pull origin master
  supervisor spice restart

* support audio?
* cache source code (add new setting key for cache dir)
  /cache/text/filename.html
  /cache/glyphs/filename-med.png
* Paging - 50 items per page or so

* export endpoint (should zip all files with correct names
  (when possible)

* sets
  - go to /set/ to create a new set, can upload multiple files and share
    one link, can also associate other files to the link

* tile view

* See if we can tweak the short-id alphabet (remove `-` and `_`)

* reasonable text describing spice
  - your host, your stuff, your shares.
  - a personal sharing service

* Move settings.cfg to settings-example.cfg - complain if not found
* readme
