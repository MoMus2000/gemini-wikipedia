import jetforce


def app(environ, send_status):
    """
    Arguments:
        environ: A dictionary containing information about the request
        send_status: A callback function that takes two parameters: The
            response status (int) and the response meta text (str).

    Returns: A generator containing the response body.
    """
    send_status(10, "text/gemini")
    yield f"Received path: {environ['GEMINI_URL']} WTF"


if __name__ == "__main__":
    server = jetforce.GeminiServer(app)
    server.run()
