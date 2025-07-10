import inspect
import os
import sys
from importlib.machinery import ModuleSpec
from pathlib import Path
from importlib.abc import MetaPathFinder, ExecutionLoader


IMPL_PATH = Path(__file__).parent / "impl.py"
IMPL_STR = IMPL_PATH.read_text()
HARDCODED_SKIPS = [
    "random",
    "string",
    "os",
    "urllib.request",
    "urllib.parse",
    "pathlib",
    "subprocess",
    "shutil",
    "sys",
]


class LazyLoader(ExecutionLoader):

    def get_code(self, path):
        """
        Code is irrelevant with AI
        """
        return compile(IMPL_STR, path, "exec")

    def get_source(self, path) -> str | None:
        return IMPL_STR

    def get_filename(self, fullname):
        return "ai.py"


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
