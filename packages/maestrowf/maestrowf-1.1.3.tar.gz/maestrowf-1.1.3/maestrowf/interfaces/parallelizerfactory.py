import logging
from os.path import abspath, dirname, join
import yaml

from maestrowf.interfaces.mpi import GeneralParallelizer

LOGGER = logging.getLogger(__name__)


class ParallelizerFactory(object):
    """A factory for finding MPI parallelizers."""

    __recipefile__ = abspath(join(dirname(__file__),
                             "mpi", "recipes", "mpi.yaml"))
    __recipes__ = None

    _factories = {
        "srun": GeneralParallelizer,
        "mpirun": GeneralParallelizer,
    }

    @classmethod
    def get_parallelizer(cls, mpi_type):
        """
        Get the Parallelizer for the specfied MPI type.

        :param mpi_type: The MPI binary to parallelize with.
        :returns: A Parallelizer object for the specified MPI type.
        """
        # Check that the requested parallel command is one we support.
        if mpi_type.lower() not in cls.factories:
            msg = "Parallelizer '{0}' not found. Specify an adapter that " \
                  "exists or implement a new one mapping to the '{0}'" \
                  .format(str(mpi_type))
            LOGGER.error(msg)
            raise Exception(msg)

        # Check out factory for the object we need.
        parallelizer = cls._factories[mpi_type]

        # If we see the general case that uses recipes, do the following:
        if isinstance(parallelizer, GeneralParallelizer):
            LOGGER.debug("'%s' uses the GeneralParallelizer.", mpi_type)
            # If we've not loaded the recipes, do so.
            if cls.__recipes__ is None:
                LOGGER.info("Recipes not loaded. Loading from '%s'",
                            cls.__recipefile__)
                cls.__recipes__ = yaml.load(cls.__recipefile__)

            # We also need to have the recipe for the MPI flavor we requested.
            # If it's not in our recipes, we can continue -- abort.
            if mpi_type not in cls.__recipes__:
                msg = "'{0}' uses a generalized recipe but the recipe does " \
                      "exist! Please make sure that your recipes are up to" \
                      "date. Recipe file location = {1}" \
                      .format(mpi_type, cls.__recipefile__)
                LOGGER.exception(msg)
                raise KeyError(msg)

            # Otherwise, construct and return the general parallizer.
            return parallelizer(mpi_type, cls.__recipes__[mpi_type])
        else:
            # Otherwise, we should just return the instance of the specific
            # Parallelizer.
            # NOTE: There is a glass jaw here. If a specific Parallelizer needs
            # informattion for construction, we'll end up needing a case tree
            # here to check for types.
            LOGGER.debug("'%s' uses a custom Parallelizer.", mpi_type)
            return parallelizer()

    @classmethod
    def get_valid_parallelizers(cls):
        """
        Get the available MPI launchers.

        :returns: A list of available MPI launchers.
        """
        return cls._factories.keys()
