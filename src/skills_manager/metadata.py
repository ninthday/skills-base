import importlib.util
from collections.abc import Mapping, Sequence
from pathlib import Path
from types import MappingProxyType, ModuleType
from uuid import uuid4

from .models import Metadata, VendorSkillMeta


class MetadataError(RuntimeError):
    """Raised when a project's editable metadata is invalid."""


def discover_project_root(start: Path) -> Path:
    """Find the nearest ancestor containing the project manifest and metadata."""
    current = start.resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "meta.py"
        ).is_file():
            return candidate

    raise MetadataError(
        f"Could not find a project root above {start} containing pyproject.toml and meta.py"
    )


def _load_module(meta_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        f"skills_manager_meta_{uuid4().hex}", meta_path
    )
    if spec is None or spec.loader is None:
        raise MetadataError(f"Could not create an import specification for {meta_path}")

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as error:
        raise MetadataError(f"Failed to import {meta_path}: {error}") from error
    return module


def _string_mapping(value: object, name: str) -> Mapping[str, str]:
    if not isinstance(value, Mapping):
        raise MetadataError(f"meta.py {name} must be a mapping")
    if not all(
        isinstance(key, str) and isinstance(item, str) for key, item in value.items()
    ):
        raise MetadataError(f"meta.py {name} must map strings to strings")
    return MappingProxyType(dict(value))


def load_metadata(root: Path) -> Metadata:
    """Load and validate the editable ``meta.py`` at ``root``."""
    meta_path = root / "meta.py"
    if not meta_path.is_file():
        raise MetadataError(f"Metadata file does not exist: {meta_path}")

    module = _load_module(meta_path)
    required_names = ("submodules", "vendors", "manual")
    missing_names = [name for name in required_names if not hasattr(module, name)]
    if missing_names:
        raise MetadataError(
            f"meta.py is missing required names: {', '.join(missing_names)}"
        )

    submodules = _string_mapping(module.submodules, "submodules")
    if not isinstance(module.vendors, Mapping):
        raise MetadataError("meta.py vendors must be a mapping")

    vendors: dict[str, VendorSkillMeta] = {}
    for vendor_name, vendor in module.vendors.items():
        if not isinstance(vendor_name, str):
            raise MetadataError("meta.py vendors must use string names")
        if not isinstance(vendor, VendorSkillMeta):
            raise MetadataError(
                f"meta.py vendors[{vendor_name!r}] must be a VendorSkillMeta instance"
            )
        if not isinstance(vendor.source, str):
            raise MetadataError(
                f"meta.py vendors[{vendor_name!r}].source must be a string"
            )
        vendors[vendor_name] = VendorSkillMeta(
            source=vendor.source,
            skills=_string_mapping(vendor.skills, f"vendors[{vendor_name!r}].skills"),
        )

    if isinstance(module.manual, str) or not isinstance(module.manual, Sequence):
        raise MetadataError("meta.py manual must be a sequence of strings")
    if not all(isinstance(name, str) for name in module.manual):
        raise MetadataError("meta.py manual must be a sequence of strings")

    return Metadata(
        submodules=submodules,
        vendors=MappingProxyType(vendors),
        manual=tuple(module.manual),
    )
