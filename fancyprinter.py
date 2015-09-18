class FancyPrinter:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print_warning(message):
        print FancyPrinter.WARNING + message + FancyPrinter.ENDC

    @staticmethod
    def print_blue(message):
        print FancyPrinter.OKBLUE + message + FancyPrinter.ENDC

    @staticmethod
    def print_green(message):
        print FancyPrinter.OKGREEN + message + FancyPrinter.ENDC

    @staticmethod
    def print_error(message):
        print FancyPrinter.FAIL + message + FancyPrinter.ENDC

    @staticmethod
    def get_warning(message):
        print FancyPrinter.WARNING + message + FancyPrinter.ENDC

    @staticmethod
    def get_blue(message):
        print FancyPrinter.OKBLUE + message + FancyPrinter.ENDC

    @staticmethod
    def get_green(message):
        print FancyPrinter.OKGREEN + message + FancyPrinter.ENDC

    @staticmethod
    def get_error(message):
        print FancyPrinter.FAIL + message + FancyPrinter.ENDC
