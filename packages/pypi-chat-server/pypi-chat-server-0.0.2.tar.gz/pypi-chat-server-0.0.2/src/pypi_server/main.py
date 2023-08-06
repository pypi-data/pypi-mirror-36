#!/usr/bin/env python

# Сервер чата

import logging

from pypi_server.core.server import Server
from pypi_server.utils import log_config
from pypi_server.utils.utils import get_params


logger = logging.getLogger("server_log")


def main():
    params = get_params()
    server = Server(*params)
    try:
        print("Сервер запущен IP: {}; PORT: {}".format(params[0], params[1]))
        print("*** Для отключения сервера используйте CTRL+C ***")
        server.start_server()
    except KeyboardInterrupt:
        server.shutdown()
        print("Всего хорошего!")
    except Exception as error:
        logger.critical('Не удалось запустить сервер: {}'.format(error))


if __name__ == "__main__":
    main()

