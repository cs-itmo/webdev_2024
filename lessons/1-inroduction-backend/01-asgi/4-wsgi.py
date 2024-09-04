def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    # show environ details
    for key, value in environ.items():
        print(f"{key}: {value}")
    start_response(status, response_headers)
    return [b"Hello, World!"]