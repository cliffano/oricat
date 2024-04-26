"""Logger for oricat."""
from conflog import Conflog

def init():
    """Initialize logger.
    """

    cfl = Conflog(
        conf_dict={
            'level': 'debug',
            'format': '[oricat] %(levelname)s %(message)s'
        }
    )

    return cfl.get_logger(__name__)
