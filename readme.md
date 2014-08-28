Spice is a personal file sharing service. It aims to be a simple and
clean alternative to cloud.app or dropbox for sharing files with
friends.

Features:

* Upload many files just by dragging and dropping them on to the page.
* Private, public, and limited (viewable by link only) sharing.
* Syntax highlight code views

Installation:

1. Checkout this repo
2. pip install pygments flask flask-login sqlalchemy
3. Copy settings-example.cfg to settings.cfg and update values
4. Create an empty database: `python runserver.py init_db`
5. Create a user: `python runserver.py user`
6. Run the dev server: `python runserver.py`

For a production environment you do the above but instead of using
`python runserver.py` to run spice you would use uswgi or your preferred
choice of python server.

Todo:

* Markdown rendering
* Handle audio files nicely
* Tile view
* File sets so you can easily share multiple files
* Add remove endpoint
* note field/custom key
* support audio?
* Caching for views (add new setting key for cache dir)
  /cache/text/filename.html
  /cache/glyphs/filename-med.png
* Paging - 50 items per page or so
* Export endpoint (should zip all files with correct names
  (when possible)
* Tile view
* See if we can tweak the short-id alphabet (remove `-` and `_`)
* Move settings.cfg to settings-example.cfg - complain if not found
