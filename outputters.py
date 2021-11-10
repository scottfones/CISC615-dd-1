from xmlproc.xmlapp import ErrorHandler


class MyErrorHandler(ErrorHandler):

    def __init__(self, locator, warnings: bool = False):
        super().__init__(locator)
        self.show_warnings = warnings
        self.errors = []
        self.warnings = []

    def location(self):
        return "%s:%d:%d" % (self.locator.get_current_sysid(),
                             self.locator.get_line(),
                             self.locator.get_column())

    def warning(self, msg):
        if self.show_warnings:
            self.warnings.append(f"W:{self.location()}: {msg}")

    def error(self, msg):
        self.fatal(msg)

    def fatal(self, msg):
        self.errors.append(f"E:{self.location()}: {msg}")

    def reset(self):
        """Clear errors and warnings."""
        self.errors = []
        self.warnings = []
