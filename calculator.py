"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!
"""

import re
from functools import reduce

def add(*args):
    adding = reduce((lambda x, y: x + y), [int(i) for i in args])
    return str(adding)

def subtract(*args):
    subtracting = reduce((lambda x, y: x - y), [int(i) for i in args])
    return str(subtracting)

def multiply(*args):
    multiplying = reduce((lambda x, y: x * y), [int(i) for i in args])
    return str(multiplying)

def divide(*args):
    dividing = reduce((lambda x, y: x / y), [int(i) for i in args])
    return str(dividing)


def how_to(*args):

  return  """<html>
    <head><strong>Lesson 4 Assignment: WSGI Calculator</strong></head>
    <p><strong>How-Tos:</strong></p>
    <p><strong>Copying and pasting the following URL by the specific math opetation</strong></p>
    <ol>
      <li><strong>Addition:</strong> http://localhost:8080/add/23/42</li>
      <li><strong>Subtraction:</strong> http://localhost:8080/subtract/23/42</li>
      <li><strong>Multiplication:</strong> http://localhost:8080/multiply/3/5</li>
      <li><strong>Division:</strong> http://localhost:8080/divide/22/11</li>
    </ol>
    </html>
    """

def resolve_path(path):

    # Vamsi's sample code.

    funcs = {

      '': how_to,
      'add': add,
      'subtract': subtract,
      'multiply': multiply,
      'divide': divide,
    }


    path = path.strip('/').split('/')

    func = funcs[path[0]]

    args = path[1:]

    return func, args    


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.

    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Not Found</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()   
