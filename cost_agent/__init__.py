import warnings

from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings(
    "ignore",
    message=r".*\[EXPERIMENTAL\].*",
    category=UserWarning,
)

from shared.logging_utils import configure_logging  # noqa: E402
configure_logging("scheduling_agent")

from .agent import root_agent  # noqa: E402, F401

__all__ = ["root_agent"]