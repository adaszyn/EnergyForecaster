class FancyPrinter:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def warning(self, message):
    	print self.WARNING + message + self.ENDC
    def blue(self, message):
    	print self.OKBLUE + message + self.ENDC
    def green(self, message):
    	print self.OKGREEN + message + self.ENDC
    def error(self, message):
    	print self.FAIL + message + self.ENDC 