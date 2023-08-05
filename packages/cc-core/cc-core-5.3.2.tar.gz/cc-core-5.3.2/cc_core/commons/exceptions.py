import re
from traceback import format_exc


def exception_format(secret_values=None):
    exc_text = format_exc()
    if secret_values:
        exc_text = re.sub('|'.join(secret_values), '********', exc_text)
    return [l.replace('"', '').replace("'", '') for l in exc_text.split('\n') if l]


class ArgumentError(Exception):
    pass


class AgentError(Exception):
    pass


class EngineError(Exception):
    pass


class FileError(Exception):
    pass


class JobExecutionError(Exception):
    pass


class CWLSpecificationError(Exception):
    pass


class JobSpecificationError(Exception):
    pass


class RedSpecificationError(Exception):
    pass


class RedValidationError(Exception):
    pass


class RedVariablesError(Exception):
    pass


class ConnectorError(Exception):
    pass


class AccessValidationError(Exception):
    pass


class AccessError(Exception):
    pass
