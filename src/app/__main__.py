from API.API import app, IP

if __name__ == '__main__':
    print(IP)
    app.run(port=3050, host='0.0.0.0', threaded=True)
#    app.run(port=int(IP), host='0.0.0.0', threaded=True)
