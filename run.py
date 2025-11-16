import os

from app import create_app

app =  create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    host = os.environ.get('HOST', '127.0.0.1')
    app.run(debug=True, port=port, host=host)

