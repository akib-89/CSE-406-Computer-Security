# this is the router class of the crypto system

import os
import socket
import json
# class Router
# this class is the router of the crypto system


class Router:
    # the path of the router
    path = None

    # socket
    socket = None

    # __init__
    def __init__(self, socket, path):
        """
        this method is the constructor of the router class
        @param path the path of the router
        """
        self.path = path
        self.socket = socket

    # get_path
    def get_path(self):
        return self.path

    # route
    def route(self):
        """
        this method is the default router method
        depending on the path set on the constructor(__init__)
        method, this method will route the request to the
        appropriate controller
        """
        dummy_response = "<html>\
            <head>\
            <title>404 Not Found</title>\
            </head>\
            <body>\
            <h1>Not Found</h1>\
            <p>The requested URL was not found on the server.\
            If you entered the URL manually please check your\
            spelling and try again.</p>\
            </body>\
            </html>"

        # seperate path from the query params
        path = self.path.split("?")[0]

        # extract the query params if any
        # check if there are any query params
        query_params = {}
        if len(self.path.split("?")) > 1:
            # extract the query params
            query_params = self.path.split("?")[1]
            # split the query params
            query_params = query_params.split("&")
            # create a dictionary
            query_params = dict(
                map(lambda x: x.split("="), query_params))

        print(query_params)

        # if the route is /public/get_parameters
        if path == "/public/get_parameters":
            # import the public controller
            from public_controller import PublicController

            # create the public controller
            public_controller = PublicController()

            # call the get_parameters method
            response = public_controller.get_parameters()

            # send the response
            self.send_json_response(str(response))

        elif path == "/unauth/register":
            # import the unauth controller
            from unauth_controller import UnauthController

            # register the user
            response = UnauthController().register(
                query_params["username"], query_params["public_key"])

            # send the response
            self.send_json_response(str(response))

        else:
            # send a dummy response
            self.send_html_response(dummy_response)

    def send_html_response(self, response):
        """
        this method sends the response to the client
        @param response the response to send
        """
        # Send the response headers
        headers = [
            'HTTP/1.1 200 OK',
            'Content-Type: text/html; charset=utf-8',
            'Content-Length: {}'.format(len(response)),
            'Connection: close',
            '\r\n',
        ]
        response_headers = '\r\n'.join(headers)
        self.send_response(response_headers, response)

    def send_json_response(self, response):
        """
        this method sends the response to the client
        @param response the response to send
        """
        # convert the response to json
        json_response = json.dumps(
            response, sort_keys=True, indent=4, separators=(',', ': '))

        print(json_response)
        # Send the response headers
        headers = [
            'HTTP/1.1 200 OK',
            'Content-Type: application/json',
            'Content-Length: {}'.format(len(json_response)),
            'Connection: close',
            '\r\n',
        ]

        response_headers = '\r\n'.join(headers)
        self.send_response(response_headers, json_response)

    def send_conflict_json_response(self, response):
        """
        this method sends the response to the client
        @param response the response to send
        """
        # convert the response to json
        json_response = json.dumps(
            response, sort_keys=True, indent=4, separators=(',', ': '))

        print(json_response)
        # Send the response headers
        headers = [
            'HTTP/1.1 409 Conflict',
            'Content-Type: application/json',
            'Content-Length: {}'.format(len(json_response)),
            'Connection: close',
            '\r\n',
        ]

        response_headers = '\r\n'.join(headers)
        self.send_response(response_headers, json_response)

    def send_response(self, headers, response):
        """
        this method sends the response to the client
        @param response the response to send
        """

        self.socket.sendall(headers.encode())

        # Send the response body
        self.socket.sendall(response.encode())

        # Close the socket
        self.socket.close()
