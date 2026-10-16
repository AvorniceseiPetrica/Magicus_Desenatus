from dataclasses import dataclass
from models.objects.spell import PropagationType, SpellPropagation


@dataclass(frozen=True)
class SpellRules:  # all balance numbers in one injectable place
    self_step: int = 1  # "short distance" per arrow
    directional_step: int = 3  # "longer distance" per arrow
    aoe_radius: int = 1
    cost_per_arrow: int = 1
    directional_surcharge: int = 1
    aoe_surcharge: int = 2
    mana_regen: int = 1

    def step_length(self, p: SpellPropagation) -> int:
        return self.self_step if p.type is PropagationType.SELF else self.directional_step

    def mana_cost(self, p: SpellPropagation) -> int:
        cost = len(p.directions) * self.cost_per_arrow
        if p.type is PropagationType.DIRECTIONAL:
            cost += self.directional_surcharge
            if p.aoe_at_end:
                cost += self.aoe_surcharge
        return cost
