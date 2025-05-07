# storm/common/interfaces/modules/module_metadata.py

from dataclasses import dataclass, field
from typing import Any, List, Optional, Type


@dataclass
class ModuleMetadata:
    imports: Optional[List[Any]] = field(default_factory=list)
    controllers: Optional[List[Type]] = field(default_factory=list)
    providers: Optional[List[Any]] = field(default_factory=list)
    exports: Optional[List[Any]] = field(default_factory=list)
