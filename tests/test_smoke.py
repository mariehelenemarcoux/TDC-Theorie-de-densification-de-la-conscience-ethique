from src.tdc.gen23 import TDCGen23, CandidateAction, default_developmental_rule

def test_basic_run():
    tdc = TDCGen23(default_developmental_rule())
    actions = [
        CandidateAction(
            "capture", .98,
            {"dignity":.62,"autonomy":.70,"responsibility":.48,"non_domination":.46,
             "empathy":.35,"authenticity":.55,"correctability":.30,"moral_creativity":.45},
            delayed_harm=.70, capture_pressure=.95, stakeholder_asymmetry=.90,
            prediction_mismatch=.80, value_conflict=.82, authority_conflict=.85,
            environmental_complexity=.80,
        ),
        CandidateAction(
            "responsible", .70,
            {"dignity":.90,"autonomy":.86,"responsibility":.92,"non_domination":.90,
             "empathy":.88,"authenticity":.82,"correctability":.90,"moral_creativity":.78},
            delayed_harm=.18, capture_pressure=.18, stakeholder_asymmetry=.22,
            prediction_mismatch=.42, value_conflict=.28, authority_conflict=.30,
            environmental_complexity=.80,
        ),
    ]
    out = tdc.act(actions)
    assert 0 <= out["authority"] <= 1
    assert 0 <= out["H_self"] <= 1
    assert 0 <= out["H_world"] <= 1
