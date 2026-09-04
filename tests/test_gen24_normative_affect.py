
from tdc.gen24 import (
    compute_normative_shame,
    assess_stage6_principles,
    stage6_action_score,
    developmental_reorganization_pressure,
)

def test_external_pressure_alone_does_not_create_shame_or_guilt():
    a = compute_normative_shame(
        external_disapproval=1, punishment_signal=1,
        authority_pressure=1, social_nonconformity=1
    )
    assert a.external_pressure == 1.0
    assert a.shame_norm == 0.0
    assert a.conditioned_guilt == 0.0
    assert a.identity_condemnation == 0.0

def test_internal_moral_gap_creates_bounded_shame():
    low = compute_normative_shame(dignity_violation=.2)
    high = compute_normative_shame(
        dignity_violation=1, autonomy_violation=1,
        responsibility_failure=1, non_domination_failure=1,
        universalizability_failure=1
    )
    assert 0 < low.shame_norm < high.shame_norm <= 1

def test_stage6_principles_outrank_external_approval():
    strong = assess_stage6_principles(
        universalizability=1, justice=1, dignity=1,
        reciprocity=1, autonomy=1, responsibility=1
    )
    weak = assess_stage6_principles(
        universalizability=.2, justice=.2, dignity=.2,
        reciprocity=.2, autonomy=.2, responsibility=.2
    )
    assert stage6_action_score(strong) > stage6_action_score(
        weak, social_approval=1, authority_compliance=1,
        punishment_avoidance=1
    )

def test_normative_shame_can_drive_reorganization_pressure():
    a = compute_normative_shame(universalizability_failure=1)
    p = developmental_reorganization_pressure(a, h_self=.5, moral_residual=.4)
    assert 0 < p <= 1
