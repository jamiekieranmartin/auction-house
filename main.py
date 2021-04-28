import os
from auction import create_app

if __name__ == '__main__':
    host = None

    if 'HOST' in os.environ:
        host = os.environ['HOST']

    app = create_app()
    app.run(host, debug=True)
