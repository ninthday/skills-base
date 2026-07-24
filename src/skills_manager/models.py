from collections.abc import Mapping, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class VendorSkillMeta:
    source: str
    skills: Mapping[str, str]


@dataclass(frozen=True)
class Metadata:
    submodules: Mapping[str, str]
    vendors: Mapping[str, VendorSkillMeta]
    manual: Sequence[str]
