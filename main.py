import json
import tornado.log

from tornado.gen import coroutine, Return
from tornado.options import define, options
from hash import identify_hashes


class MainHandler(tornado.web.RequestHandler):
    """ Creates a JSON API """

    def data_received(self, chunk):
        pass

    def intialise(self):
        self.set_header("Server", "HashID")
        self.set_header("X-Content-Type-Options", "nosniff")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST")

    @coroutine
    def identify_hashes(self, hsh):
        # Wrapper function
        raise Return(identify_hashes(hsh))

    @coroutine
    def get(self, *args):
        # Identifies a single hash
        results = yield self.identify_hashes(args[0])
        self.write({args[0]: results})

    @coroutine
    def post(self, *args):
        response = {}
        try:
            hashes = json.loads(self.request.body)['hashes']
            for hsh in set(hashes):
                response[hsh] = yield self.identify_hashes(hsh)
        except ValueError:
            response = {'error': 'could not parse statement'}
        self.write(response)


application = tornado.web.Application([
    (r"/(.*", MainHandler),
])

define("port",
       default="8888",
       type=int,
       help="the listen port for the web server"
       )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
