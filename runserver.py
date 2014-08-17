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

else:
  from spice import app
  app.run(debug=True, host='0.0.0.0')

  import spice.views
