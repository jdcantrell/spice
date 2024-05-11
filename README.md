# Spice

Spice is a personal file sharing service. It aims to be a simple and
clean alternative to cloud.app or dropbox for sharing files with
friends.

## Todo:

- find right way for package to support cli
- update readme
  - initial setup
  - deploy steps

## Maybe someday

- Handle audio files nicely
- Export endpoint (should zip all files with correct names
  (when possible)
- File sets so you can easily share multiple files
- note field/custom key
- See if we can tweak the short-id alphabet (remove `-` and `_`)

## Features:

- Upload many files just by dragging and dropping them on to the page.
- Upload files via cut and paste
- Private, public, and limited (viewable by link only) sharing.
- Syntax highlight code views

## Initial setup:

1. Checkout this repo
2. `pipenv install`
3. Copy settings-example.cfg to settings.cfg and update values
4. Export flask env vars:
   export FLASK_APP=spice
   export FLASK_ENV=development
5. Initialize database: `flask init-db`
6. Create a user: `flask create-user`
7. Run the dev server: `flask run`

For production you will want to use something besides flask to run the server.
This repo includes a spice.service file that uses uwsgi, you can update the
paths and copy that to `/lib/systemd/service/` and then you should be able to
do:

```
systemctl daemon-reload
systemctl enable spice
systemctl start spice
```
