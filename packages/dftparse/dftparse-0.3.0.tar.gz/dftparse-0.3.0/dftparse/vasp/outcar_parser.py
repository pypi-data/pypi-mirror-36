from ..core import BlockParser


def _parse_total_magnetization(line, lines):
    """Parse the total magnetization, which is somewhat hidden"""
    toks = line.split()
    res = {"number of electrons": float(toks[3])}
    if len(toks) > 5:
        res["total magnetization"] = float(toks[5])
    return res

def _parse_volume_of_cell(line, lines):
    """Parse the volume of the unit cell"""
    return {"volume of cell": float(line.split()[4])}

base_rules = [
    (lambda x: " number of electron " in x, _parse_total_magnetization),
    (lambda x: " volume of cell " in x, _parse_volume_of_cell)
]


class OutcarParser(BlockParser):
    """Parser for VASP's OUTCAR file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
