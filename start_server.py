from waitress import serve

from board_resolution_is.wsgi import application

if __name__ == '__main__':
    serve(application, port='5400')
