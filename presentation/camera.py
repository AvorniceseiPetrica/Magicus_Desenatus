def camera_origin(focus: float, view: int, world: int) -> float:
    """Marginea stângă/de sus a camerei, în tile-uri, cu `focus` în centru.

    Harta mai mare decât viewport-ul: camera se oprește la margini.
    Harta mai mică: valoare negativă, deci harta apare centrată.
    """
    if world <= view:
        return (world - view) / 2
    return min(max(focus + 0.5 - view / 2, 0.0), world - view)