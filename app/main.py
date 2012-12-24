
import orl_settings

import sys
import os
import mongoengine
from tornado import web, ioloop
from tornado.options import define, options, parse_command_line

config = orl_settings.ORLSettings()
settings = {
        'debug': config.debug,
        'cookie_secret': config.cookie_secret,
        'template_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
        'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
        'login_url': '/login',
}

application = web.Application([
    (r'/', 'home.HomeHandler'),
    (r'/login', 'login.LoginHandler'),
    (r'/logout', 'login.LogoutHandler'),
    (r'/register', 'login.RegisterHandler'),
    (r'/dashboard', 'dashboard.DashboardHandler'),
    (r'/add', 'runs.AddRunHandler'),
], **settings)

application.config = config



if __name__ == '__main__':
    define('port', default=11000, help='TCP port to listen on')
    parse_command_line()

    mongoengine.connect(
            application.config.db_name, 
            host=application.config.db_host, 
            port=application.config.db_port, 
            username=application.config.db_username, 
            password=application.config.db_password)

    application.listen(options.port)
    ioloop.IOLoop.instance().start()

