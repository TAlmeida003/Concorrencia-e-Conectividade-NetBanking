from API.API import app, PORT

if __name__ == '__main__':
    app.run(port=int(PORT), host='0.0.0.0', threaded=True)
