import sys

if len(sys.argv) > 1:
  if sys.argv[1] == 'user':
    from spice.models import User
    from spice.database import db_session
    name = raw_input('User name: ')
    password = raw_input('Password: ')

    user = User(name, password)

    db_session.add(user)
    db_session.commit()



    print 'User created: %r' % user.id

  if sys.argv[1] == 'init_db':
    from spice import app
    from spice.database import init_db
    init_db()

    print "Database init"

  if sys.argv[1] == 'process':
    from spice.models import File
    from spice.database import db_session
    from spice.handlers import get_handler, get_handler_instance
    files = db_session.query(File).order_by(File.id.desc()).all()

    for record in files:
      handler = get_handler_instance(record)
      handler.process()
      db_session.add(handler.record)

    db_session.commit()

else:
  from spice import app
  app.run(debug=True, host='0.0.0.0')

  import spice.views
