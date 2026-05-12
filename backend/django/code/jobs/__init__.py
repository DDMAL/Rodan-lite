import logging
import importlib

logger = logging.getLogger("rodan")


def module_loader(name, callback=lambda m: None):
    try:
        logger.info("Importing: " + name)
        m = importlib.import_module(name)
        callback(m)
    except ModuleNotFoundError as e:
        if e.name == name or (e.name and e.name.startswith(name)):
            logger.warning("Skipping missing module {0}: {1}".format(name, e))
        else:
            raise ImportError("Trouble loading module {0}.\nMessage: {1}".format(name, e))
    except ImportError as e:
        raise ImportError("Trouble loading module {0}.\nMessage: {1}".format(name, e))


package_versions = {}
