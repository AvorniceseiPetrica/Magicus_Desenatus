from models.objects.entity import Entity
from models.objects.spell import PropagationType, SpellAffinity, SpellCast, SpellPropagation
from business.application.commands import SpellKind, SpellRequest


class SpellCastFactory:
    def create(self, caster: Entity, request: SpellRequest) -> SpellCast:
        ptype = PropagationType.SELF if request.kind is SpellKind.SELF else PropagationType.DIRECTIONAL
        return SpellCast(
            caster,
            SpellAffinity(request.affinity),
            SpellPropagation(ptype, request.directions,
                             aoe_at_end=request.kind is SpellKind.DIRECTIONAL_AOE),
        )
