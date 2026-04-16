import sys
import os

class Logger:
    BASE_DIR: str

    class _level:
        NOTSET = 0
        INFO = 1
        DEBUG = 2
        WARNING = 3
        ERROR = 4
        CRITICAL = 5

    _level_str = {
        _level.NOTSET : "NOT SET",
        _level.INFO : "INFO",
        _level.DEBUG : "DEBUG",
        _level.WARNING : "WARNING",
        _level.ERROR : "ERROR",
        _level.CRITICAL : "CRITICAL",
    }



    def __init__(self):
        self.BASE_DIR = os.getcwd()

        self.Info(f"logger initialized in {self.BASE_DIR}", False)


    def _print(self, msg, level = _level.NOTSET, verbose = True):
        # TODO: can analyze the details by creating exception and parsing that

        # caller = sys._getframe(2) # the function that called info
        # line = caller.f_lineno
        # file = caller.f_code.co_filename
        # func = caller.f_code.co_name

        # file_local = file.replace(self.BASE_DIR, "")

        # details =  f"[{self._level_str[level]}]"
        # if verbose:
        #     details += f"{file_local}:{line} in {func}() "

        print(f"[{self._level_str[level]}]: {msg}")


    # TODO:
    # NOTE: must also check with remaining memory or remove logs after a while
    # also save time
    def _write_to_file():
        pass


    def Info(self, msg, verbose = False): # NOTE: info is the only one to be default non verbose
        self._print(msg, level = self._level.INFO, verbose = verbose)

    def Debug(self, msg, verbose = True):
        self._print(msg, level = self._level.DEBUG, verbose = verbose)

    def Warning(self, msg, verbose = True):
        self._print(msg, level = self._level.WARNING, verbose = verbose)

    def Error(self, msg, verbose = True):
        self._print(msg, level = self._level.ERROR, verbose = verbose)

    def Critical(self, msg, verbose = True):
        self._print(msg, level = self._level.CRITICAL, verbose = verbose)



if __name__ == "__main__":

    def somefunc():
        logger = Logger()
        logger.Error("yo")

    somefunc()
