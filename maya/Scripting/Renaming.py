import re
from typing import Sequence, Dict, Optional, Tuple
try:
    import maya.cmds as cmds
except Exception:
    cmds = None

def _find_hash_run(pattern: str) -> Tuple[int, int]:
    m = re.search(r"(#+)", pattern)
    if not m:
        raise ValueError("Pattern must contain at least one '#' character to indicate numbering")
    return m.start(1), len(m.group(1))

def _build_name(pattern: str, num: int, width: int) -> str:
    """Build name by replacing the first run of #'s with zero-padded number."""
    fmt = f"{{:0{width}d}}"
    num_str = fmt.format(num)
    return re.sub(r"(#+)", num_str, pattern, count=1)

def rename_nodes(pattern: str,
                 start: int = 1,
                 step: int = 1,
                 nodes: Optional[Sequence[str]] = None,
                 reverse: bool = False) -> Dict[str, str]:
    
    if nodes is None:
        if cmds is None:
            raise RuntimeError("No node list provided and maya.cmds not available")
        nodes = cmds.ls(selection=True, long=True) or []

    nodes = list(nodes)
    if not nodes:
        raise RuntimeError("No nodes provided or selected to rename")

    if reverse:
        nodes = list(reversed(nodes))

    # validate pattern and compute padding width
    _, hash_count = _find_hash_run(pattern)
    width = hash_count

    mapping: Dict[str, str] = {}
    current = start
    for node in nodes:
        new_name = _build_name(pattern, current, width)
        if cmds is not None:
            try:
                res = cmds.rename(node, new_name)
                mapping[node] = res
            except Exception as e:
                mapping[node] = f"<rename_failed: {e}>"
        else:
            mapping[node] = new_name
        current += step

    return mapping

def rename_selection(pattern: str, start: int = 1, step: int = 1, reverse: bool = False) -> Dict[str, str]:
    """Convenience wrapper: rename the current Maya selection with `pattern`."""
    return rename_nodes(pattern, start=start, step=step, nodes=None, reverse=reverse)

#make sure that after sending this code through you need to use rename_selection function and not rename to rename the selected objects in maya.