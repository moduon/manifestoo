from typing import Iterable, Iterator, Optional, Set, Tuple

from .addon import Addon
from .addons_selection import AddonsSelection
from .addons_set import AddonsSet


def dependency_iterator(
    addons_selection: AddonsSelection,
    addons_set: AddonsSet,
    recursive: bool,
) -> Iterator[Tuple[str, Optional[Addon]]]:
    """Iterate addons and their dependencies.

    Yield tuples:
    - addon name
    - addon object (None if not found in addons_set)

    If recursive is False, only yield addon_selection.

    An addon is yielded at most once.
    """
    done: Set[str] = set()

    def _iter(
        addon_names: Iterable[str],
    ) -> Iterator[Tuple[str, Optional[Addon]]]:
        done.update(addon_names)
        for addon_name in addon_names:
            addon = addons_set.get(addon_name)
            yield addon_name, addon
            if recursive and addon:
                depends = addon.manifest.get("depends", [])
                yield from _iter(set(depends) - done)

    yield from _iter(addons_selection)