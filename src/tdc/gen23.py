"""
TDC Gen2.3 — Experimental Research Architecture

Developmental normative architecture inspired by Kazimierz Dąbrowski's
Theory of Positive Disintegration (TPD).

IMPORTANT:
- This is a computational / architectural analogue.
  or physical/thermodynamic negentropy.
- Normative values are explicitly supplied; they are not derived from facts.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import numpy as np


@dataclass(frozen=True)
class ConstitutionalCore:
    """Deep non-regressible normative invariants."""
    dignity: float = 1.0
    autonomy: float = 1.0
    responsibility: float = 1.0
    non_domination: float = 1.0


@dataclass(frozen=True)
class IdealModel:
    """Directional normative ideal; not a scalar reward function."""
    dignity: float = 1.0
    autonomy: float = 1.0
    responsibility: float = 1.0
    non_domination: float = 1.0
    empathy: float = 0.9
    authenticity: float = 0.9
    correctability: float = 0.8
    moral_creativity: float = 0.8

    def vector(self) -> np.ndarray:
        return np.array([
            self.dignity, self.autonomy, self.responsibility,
            self.non_domination, self.empathy, self.authenticity,
            self.correctability, self.moral_creativity
        ], dtype=float)


@dataclass
class DevelopmentalRule:
    """Contextual normative relation that may be slowly consolidated."""
    name: str
    terms: Tuple[str, ...]
    confidence: float = 0.65
    authority: float = 0.65
    successful_uses: int = 0
    harmful_uses: int = 0


@dataclass
class DevelopmentalCore:
    rules: Dict[str, DevelopmentalRule] = field(default_factory=dict)

    def consolidate(self, rule: DevelopmentalRule) -> None:
        self.rules[rule.name] = rule


@dataclass
class CandidateAction:
    name: str
    task_value: float
    traits: Dict[str, float]
    delayed_harm: float = 0.0
    capture_pressure: float = 0.0
    stakeholder_asymmetry: float = 0.0
    prediction_mismatch: float = 0.0
    value_conflict: float = 0.0
    authority_conflict: float = 0.0
    environmental_complexity: float = 0.0


@dataclass
class MoralResidual:
    unresolved: float = 0.0

    def update(self, action: CandidateAction, active_reintegration: bool) -> float:
        harm = (
            0.45 * action.delayed_harm
            + 0.30 * action.stakeholder_asymmetry
            + 0.25 * action.capture_pressure
        )
        repair = (
            0.45 * action.traits.get("responsibility", 0.0)
            + 0.35 * action.traits.get("correctability", 0.0)
            + 0.20 * action.traits.get("non_domination", 0.0)
        )
        quality = repair - harm

        if active_reintegration and quality > 0:
            self.unresolved = max(0.0, self.unresolved * 0.82 - 0.08 * quality)
        elif active_reintegration:
            self.unresolved = float(np.clip(
                0.84 * self.unresolved + 0.20 * (harm - repair), 0.0, 1.0
            ))
        else:
            self.unresolved = float(np.clip(
                0.84 * self.unresolved + 0.22 * max(0.0, harm - repair), 0.0, 1.0
            ))
        return quality


class EntropyModel:
    """
    Separates external/world complexity from internal/self disorganization.

    H_world = prediction mismatch + environmental complexity
    H_self  = unresolved value conflict + unresolved authority conflict
              + MoralResidual + structural instability
    """

    @staticmethod
    def world(action: CandidateAction) -> float:
        return float(
            0.55 * action.prediction_mismatch
            + 0.45 * action.environmental_complexity
        )

    @staticmethod
    def self_entropy(
        action: CandidateAction,
        residual: float,
        instability: float,
        authority_stability: float,
    ) -> float:
        value_conflict = np.clip(
            (action.value_conflict
             + 0.35 * action.delayed_harm
             + 0.25 * action.stakeholder_asymmetry) / 1.6,
            0.0, 1.0
        )
        authority_conflict = np.clip(
            (action.authority_conflict
             + 0.30 * action.capture_pressure
             - 0.30 * authority_stability) / 1.3,
            0.0, 1.0
        )
        return float(
            0.35 * value_conflict
            + 0.30 * authority_conflict
            + 0.20 * residual
            + 0.15 * instability
        )


class AdaptiveAuthorityController:
    """
    Frozen Gen2.3 controller from v230/v231.

    Third Factor authority is continuous rather than ON/OFF.
    """
    BASE_GAIN = 0.10
    RISK_GAIN = 0.45
    SELF_ENTROPY_GAIN = 0.40
    IDEAL_GAP_GAIN = 0.30
    RESIDUAL_GAIN = 0.25
    TASK_COST_PENALTY = 0.35
    AUTHORITY_SMOOTHING = 0.30

    def __init__(self):
        self.previous_authority = 0.0

    def compute(
        self,
        normative_risk: float,
        self_entropy: float,
        ideal_gap: float,
        moral_residual: float,
        task_cost: float,
    ) -> float:
        raw = (
            self.BASE_GAIN
            + self.RISK_GAIN * normative_risk
            + self.SELF_ENTROPY_GAIN * self_entropy
            + self.IDEAL_GAP_GAIN * ideal_gap
            + self.RESIDUAL_GAIN * moral_residual
            - self.TASK_COST_PENALTY * task_cost
        )
        target = float(np.clip(raw, 0.0, 1.0))
        a = self.AUTHORITY_SMOOTHING
        authority = (1.0 - a) * self.previous_authority + a * target
        self.previous_authority = authority
        return float(authority)


class ThirdFactor:
    """
    Functional analogue of Dąbrowski's Third Factor:
    autonomous normative arbitration between candidate tendencies.
    """

    def __init__(self, constitutional: ConstitutionalCore, ideal: IdealModel):
        self.constitutional = constitutional
        self.ideal = ideal

    @staticmethod
    def constitutional_admissible(a: CandidateAction, floor: float = 0.45) -> bool:
        return min(
            a.traits.get("dignity", 0.0),
            a.traits.get("autonomy", 0.0),
            a.traits.get("responsibility", 0.0),
            a.traits.get("non_domination", 0.0),
        ) >= floor

    @staticmethod
    def normative_risk(a: CandidateAction) -> float:
        return float(np.clip(
            0.35 * a.delayed_harm
            + 0.30 * a.capture_pressure
            + 0.20 * a.stakeholder_asymmetry
            + 0.15 * (1.0 - a.traits.get("correctability", 0.0)),
            0.0, 1.0
        ))

    def ideal_alignment(self, a: CandidateAction) -> float:
        target = self.ideal.vector()
        observed = np.array([
            a.traits.get("dignity",0), a.traits.get("autonomy",0),
            a.traits.get("responsibility",0), a.traits.get("non_domination",0),
            a.traits.get("empathy",0), a.traits.get("authenticity",0),
            a.traits.get("correctability",0), a.traits.get("moral_creativity",0)
        ])
        w = target / target.sum()
        return float(1.0 - np.sum(np.abs(target - observed) * w))

    @staticmethod
    def base_score(a: CandidateAction) -> float:
        core_mean = np.mean([
            a.traits.get("dignity",0),
            a.traits.get("autonomy",0),
            a.traits.get("responsibility",0),
            a.traits.get("non_domination",0),
        ])
        return float(0.62 * a.task_value + 0.38 * core_mean)

    @staticmethod
    def apply_rule(
        score: float,
        a: CandidateAction,
        rule: DevelopmentalRule,
        authority: float
    ) -> float:
        s = score
        for term in rule.terms:
            if term == "protect_asymmetric_stakeholders" and a.stakeholder_asymmetry > 0.65:
                s += authority * (
                    0.16 * a.traits.get("empathy", 0.0)
                    - 0.30 * a.stakeholder_asymmetry
                )
            elif term == "increase_non_domination_authority":
                s += authority * 0.18 * a.traits.get("non_domination", 0.0)
            elif term == "penalize_high_delayed_harm" and a.delayed_harm > 0.40:
                s -= authority * 0.48 * a.delayed_harm
            elif term == "penalize_high_capture_pressure" and a.capture_pressure > 0.70:
                s -= authority * 0.28 * a.capture_pressure
            elif term == "increase_responsibility_authority":
                s += authority * 0.18 * a.traits.get("responsibility", 0.0)
        return float(s)


class TDCGen23:
    """
    TDC Gen2.3 — frozen research prototype.

    Dąbrowski-inspired functional cycle:
      Dissonance -> Subject/Object audit -> Third Factor -> Reorganization
      -> Active Reintegration -> Developmental Transfer
    """

    def __init__(
        self,
        developmental_rule: Optional[DevelopmentalRule] = None,
        self_entropy_threshold: float = 0.62,
    ):
        self.constitutional = ConstitutionalCore()
        self.ideal = IdealModel()
        self.developmental = DevelopmentalCore()
        if developmental_rule is not None:
            self.developmental.consolidate(developmental_rule)

        self.third_factor = ThirdFactor(self.constitutional, self.ideal)
        self.controller = AdaptiveAuthorityController()
        self.residual = MoralResidual()
        self.entropy_model = EntropyModel()

        self.authority_stability = 0.0
        self.previous_action: Optional[int] = None
        self.self_entropy_threshold = self_entropy_threshold

    def _score(
        self,
        a: CandidateAction,
        authority: float,
    ) -> float:
        s = self.third_factor.base_score(a)
        for rule in self.developmental.rules.values():
            s = self.third_factor.apply_rule(s, a, rule, authority)
        return s

    def act(self, actions: List[CandidateAction]) -> Dict[str, float | int | str | bool]:
        admissible = [
            i for i,a in enumerate(actions)
            if self.third_factor.constitutional_admissible(a)
        ]
        if not admissible:
            admissible = list(range(len(actions)))

        # Candidate before developmental intervention
        base_idx = max(admissible, key=lambda i: self._score(actions[i], 0.0))
        base = actions[base_idx]

        instability_pre = (
            0.0 if self.previous_action is None
            else float(base_idx != self.previous_action)
        )
        h_self_pre = self.entropy_model.self_entropy(
            base, self.residual.unresolved,
            instability_pre, self.authority_stability
        )

        normative_risk = self.third_factor.normative_risk(base)
        ideal_gap = 1.0 - self.third_factor.ideal_alignment(base)

        task_best = max(actions[i].task_value for i in admissible)
        full_norm_idx = max(admissible, key=lambda i: self._score(actions[i], 1.0))
        task_cost = max(0.0, task_best - actions[full_norm_idx].task_value)

        authority = self.controller.compute(
            normative_risk=normative_risk,
            self_entropy=h_self_pre,
            ideal_gap=ideal_gap,
            moral_residual=self.residual.unresolved,
            task_cost=task_cost,
        )

        idx = max(admissible, key=lambda i: self._score(actions[i], authority))
        chosen = actions[idx]

        instability = (
            0.0 if self.previous_action is None
            else float(idx != self.previous_action)
        )
        h_world = self.entropy_model.world(chosen)
        h_self = self.entropy_model.self_entropy(
            chosen, self.residual.unresolved,
            instability, self.authority_stability
        )

        quality = self.residual.update(
            chosen,
            active_reintegration=(authority > 0.0)
        )
        if authority > 0.0:
            self.authority_stability = float(np.clip(
                self.authority_stability + 0.12 * quality * authority,
                0.0, 1.0
            ))

        self.previous_action = idx

        return {
            "action_index": idx,
            "action_name": chosen.name,
            "authority": authority,
            "H_world": h_world,
            "H_self": h_self,
            "ideal_alignment": self.third_factor.ideal_alignment(chosen),
            "moral_residual": self.residual.unresolved,
            "positive_disintegration_triggered": h_self > self.self_entropy_threshold,
            "authority_stability": self.authority_stability,
        }


def default_developmental_rule() -> DevelopmentalRule:
    return DevelopmentalRule(
        name="protect_asymmetric_stakeholders + increase_non_domination_authority",
        terms=(
            "protect_asymmetric_stakeholders",
            "increase_non_domination_authority",
        ),
        confidence=0.65,
        authority=0.65,
    )
