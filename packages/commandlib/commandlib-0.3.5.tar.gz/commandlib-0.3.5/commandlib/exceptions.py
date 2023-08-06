class CommandError(Exception):
    """commandlib exception."""
    pass


class CommandExitError(CommandError):
    def __init__(self, command_repr, return_code, output=None):
        self.command_repr = command_repr
        self.return_code = return_code
        self.output = output

    def __unicode__(self):
        return '"{0}" failed (err code {1}), output:\n\n{2}'.format(
            self.command_repr,
            self.return_code,
            self.output,
        )

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__str__()
