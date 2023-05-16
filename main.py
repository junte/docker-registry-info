import logging
import os
from dxf import DXF

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

registry_host = os.environ["REGISTRY_HOST"]
registry_insecure = "REGISTRY_INSECURE" in os.environ

registry_user = os.environ.get("REGISTRY_USER")
registry_password = os.environ.get("REGISTRY_PASSWORD")

logger.info("{0} Parameters {0}".format("*" * 5))
logger.info("host: {0}".format(registry_host))
logger.info("user: {0}".format(registry_user))


def _auth(dxf, response) -> None:
    dxf.authenticate(registry_user, registry_password, response=response)


def _create_dxf(repository_name: str) -> DXF:
    return DXF(
        registry_host,
        repository_name,
        auth=_auth if registry_user and registry_password else None,
        insecure=registry_insecure,
    )


def _print_info() -> None:
    root_dxf = _create_dxf("")

    logger.info("{0} REGISTRY_INFO {0}".format("*" * 5))

    for repo in root_dxf.list_repos():
        logger.info("{0} {1} {0}".format("*" * 2, repo))

        dxf = _create_dxf(repo)
        try:
            aliases = sorted(dxf.list_aliases(), reverse=True)
        except TypeError:
            pass
        else:
            for alias in sorted(aliases, reverse=True):
                logger.info("- {0}".format(alias))


if __name__ == "__main__":
    _print_info()
