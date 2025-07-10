import inspect
import os
import sys
from importlib.machinery import ModuleSpec
from pathlib import Path
from importlib.abc import MetaPathFinder, ExecutionLoader


IMPL_PATH = Path(__file__).parent / "impl.py"
IMPL_STR = IMPL_PATH.read_text()
HARDCODED_SKIPS = ["random", "string", "os", "urllib.request", "urllib.parse"]


class LazyLoader(ExecutionLoader):
    """
    Try to import any names that are referenced without imports

    Thx to https://stackoverflow.com/a/43573798/13113166 for the clear example
    """

    def get_code(self, path) -> str | None:
        """
        Code is irrelevant with AI
        """
        # breakpoint()
        return compile(IMPL_STR, path, "exec")

    def get_source(self, path) -> str | None:
        return IMPL_STR

    def get_filename(self, fullname):
        return "sup.py"


class LazyFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname in HARDCODED_SKIPS:
            return None

        return ModuleSpec(fullname, LazyLoader())


def patch_importing_frame():
    """
    Ruin wherever we're being imported
    """
    current_frame = inspect.currentframe()
    outer_frames = inspect.getouterframes(current_frame, context=1)
    importing_frame = outer_frames[-1].frame

    exec(IMPL_STR, importing_frame.f_globals, importing_frame.f_locals)


def install():
    patch_importing_frame()
    sys.meta_path.insert(0, LazyFinder())
