# -*- coding: utf-8 -*-
"""
Simple sockjs-tornado echo application. By default will listen on port 8080.
"""
import tornado.ioloop
import tornado.web

import sockjs.tornado


class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the echo page"""
    def get(self):
        self.render('index.html')


class EchoConnection(sockjs.tornado.SockJSConnection):
    """Echo connection implementation"""
    def on_open(self, info):
        # someone joined
        print("connection opened: %s, %s" % (info, dir(info)))

    def on_message(self, message):
        # echo message
        self.send("echoed: {}".format(message))

    def on_close(self):
        print("connection closed")

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    logger = logging.getLogger()

    # 1. Create echo router
    EchoRouter = sockjs.tornado.SockJSRouter(EchoConnection, '/echo')

    # 2. Create Tornado application
    app = tornado.web.Application(
            [(r"/", IndexHandler)] + EchoRouter.urls
    )

    # 3. Make Tornado app listen on port 8080
    app.listen(8080)
    print("Start listening on port 8080...")

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
