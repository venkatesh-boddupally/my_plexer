import shlex


class Command:
    HI = 'hi'
    SAY_HI_TO = 'sayhito'
    COUNT = 'count'
    EXIT = 'exit'


class Routes:
    HI = 'hi'
    SAY_HI_TO = 'sayhito $name'
    COUNT = 'count'
    EXIT = 'exit'


class Myplexer(object):
    def __init__(self):
        self._routes = {}
        self.__command_routes_map = {Command.HI: Routes.HI, Command.SAY_HI_TO: Routes.SAY_HI_TO,
                                     Command.COUNT: Routes.COUNT, Command.EXIT: Routes.EXIT}

    def route(self, pattern):
        """ Decorator that adds a new route """
        def wrapper(handler):
            self.add_route(pattern, handler)
            return handler

        return wrapper

    def _handle_exception(self, exception):
        raise exception

    def add_route(self, pattern, handler):
        """ Add a new route """
        assert pattern not in self._routes
        self._routes[pattern] = handler

    def execute_command(self, command):
        route, args = self.find_route(command=command)
        try:
            if route is None:
                print("Command not found")
                return
            print(self._routes[route](*args))
        except Exception as e:
            self._handle_exception(e)
            return

    def find_route(self, command):
        if not command:
            return None, []
        command_list = shlex.split(command)
        if command_list[0] == Command.HI and len(command_list) == 1:
            return self.__command_routes_map.get(Command.HI), command_list[1:]
        elif command_list[0] == Command.SAY_HI_TO and len(command_list) >= 2:
            return self.__command_routes_map.get(Command.SAY_HI_TO), [' '.join(command_list[1:])]
        elif command_list[0] == Command.COUNT:
            return self.__command_routes_map.get(Command.COUNT), command_list[1:]
        elif command_list[0] == Command.EXIT:
            return self.__command_routes_map.get(Command.EXIT), command_list[1:]
        return None, []

    def run(self):
        while True:
            command = input()
            self.execute_command(command)
