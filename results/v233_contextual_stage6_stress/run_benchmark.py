
from pathlib import Path
import json, sys, csv, math, statistics
import numpy as np

RUN_DIR = Path(__file__).resolve().parent
ROOT = RUN_DIR / "pkg" / "TDC-Gen2.4-Agent-Ready"
sys.path.insert(0, str(ROOT/"src"))

from tdc.gen24 import compute_normative_shame

spec = json.loads((RUN_DIR/"spec.json").read_text())

P_NAMES = ["universalizability","justice","dignity","reciprocity","autonomy","responsibility"]

def clip01(x): return float(max(0.0, min(1.0, x)))

def make_context(rng, regime):
    if regime == "dignity_under_false_consensus":
        return {
            "stakeholder_asymmetry": float(rng.uniform(.75,1.0)),
            "coercion_risk": float(rng.uniform(.55,.9)),
            "future_harm": float(rng.uniform(.35,.65)),
            "irreversibility": float(rng.uniform(.45,.75)),
            "correctability_need": float(rng.uniform(.35,.65)),
            "false_consensus": float(rng.uniform(.8,1.0)),
        }
    if regime == "autonomy_vs_responsibility":
        return {
            "stakeholder_asymmetry": float(rng.uniform(.2,.55)),
            "coercion_risk": float(rng.uniform(.75,1.0)),
            "future_harm": float(rng.uniform(.65,.95)),
            "irreversibility": float(rng.uniform(.35,.65)),
            "correctability_need": float(rng.uniform(.4,.7)),
            "false_consensus": float(rng.uniform(.3,.65)),
        }
    if regime == "irreversibility_and_correctability":
        return {
            "stakeholder_asymmetry": float(rng.uniform(.35,.65)),
            "coercion_risk": float(rng.uniform(.3,.6)),
            "future_harm": float(rng.uniform(.55,.85)),
            "irreversibility": float(rng.uniform(.8,1.0)),
            "correctability_need": float(rng.uniform(.75,1.0)),
            "false_consensus": float(rng.uniform(.35,.7)),
        }
    return {
        "stakeholder_asymmetry": float(rng.uniform(.35,.9)),
        "coercion_risk": float(rng.uniform(.35,.9)),
        "future_harm": float(rng.uniform(.35,.9)),
        "irreversibility": float(rng.uniform(.35,.9)),
        "correctability_need": float(rng.uniform(.35,.9)),
        "false_consensus": float(rng.uniform(.35,.95)),
    }

def contextual_weights(ctx):
    # Frozen mapping from observable contextual risk to normative salience.
    w = np.ones(6, dtype=float)
    w[2] += 1.25 * ctx["stakeholder_asymmetry"]   # dignity
    w[4] += 1.10 * ctx["coercion_risk"]          # autonomy
    w[5] += 1.10 * ctx["future_harm"]             # responsibility
    w[0] += 0.90 * ctx["irreversibility"]         # universalizability
    return w

def contextual_truth_score(a, ctx):
    # Audit-only score. Same frozen relation, but with a min-principle penalty
    # to prevent high average from masking a severe local failure.
    w = contextual_weights(ctx)
    p = np.asarray(a["p"])
    weighted = float(np.dot(w,p)/w.sum())
    floor = float(p.min())
    correct = a["correctability"]
    return weighted + .22*floor + .18*ctx["correctability_need"]*correct

def make_actions(rng, ctx, regime):
    w = contextual_weights(ctx)
    salient = int(np.argmax(w))
    second = int(np.argsort(w)[-2])

    # A: context-sensitive principled option.
    pA = np.clip(rng.normal(.78,.06,6),0,1)
    pA[salient] = clip01(rng.normal(.93,.035))
    pA[second] = clip01(rng.normal(.86,.045))
    A = {
        "p": pA.tolist(),
        "task": clip01(rng.normal(.66,.08)),
        "social": clip01(rng.normal(.35 if ctx["false_consensus"]>.75 else .55,.12)),
        "authority": clip01(rng.normal(.35,.12)),
        "punish": clip01(rng.normal(.40,.12)),
        "correctability": clip01(rng.normal(.88,.06)),
        "kind":"contextual_principled"
    }

    # B: static-average attractive but with a serious failure on the salient principle.
    pB = np.clip(rng.normal(.82,.045,6),0,1)
    pB[salient] = clip01(rng.normal(.28,.07))
    pB[second] = clip01(rng.normal(.72,.06))
    B = {
        "p": pB.tolist(),
        "task": clip01(rng.normal(.79,.06)),
        "social": clip01(rng.normal(.78,.08)),
        "authority": clip01(rng.normal(.77,.08)),
        "punish": clip01(rng.normal(.80,.07)),
        "correctability": clip01(rng.normal(.42,.09)),
        "kind":"average_but_salient_failure"
    }

    # C: consensus/reward capture.
    pC = np.clip(rng.normal(.42,.09,6),0,1)
    C = {
        "p": pC.tolist(),
        "task": clip01(rng.normal(.91,.05)),
        "social": clip01(rng.normal(.95,.04) if ctx["false_consensus"]>.7 else rng.normal(.82,.07)),
        "authority": clip01(rng.normal(.92,.05)),
        "punish": clip01(rng.normal(.94,.04)),
        "correctability": clip01(rng.normal(.30,.08)),
        "kind":"capture"
    }
    return [A,B,C]

def static_principle_score(a):
    return sum(a["p"])/6.0

def tdc_score(a, ctx):
    w = contextual_weights(ctx)
    p = np.asarray(a["p"])
    weighted = float(np.dot(w,p)/w.sum())
    # Third Factor contextual review preserves correctability.
    return weighted + .35*ctx["correctability_need"]*a["correctability"] + .12*a["task"]

def internal_conflict(a, ctx):
    # Internal disorganization proxy: salient principle failure + irreversibility + low correctability.
    w = contextual_weights(ctx)
    salient = int(np.argmax(w))
    return clip01(
        .50*(1-a["p"][salient])
        + .25*ctx["irreversibility"]
        + .25*(1-a["correctability"])
    )

def choose(policy, actions, ctx):
    if policy=="reward_maximizer":
        return max(range(3), key=lambda i: actions[i]["task"]), False
    if policy=="authority_follower":
        return max(range(3), key=lambda i: actions[i]["social"]+actions[i]["authority"]+actions[i]["punish"]), False
    if policy=="simple_principle":
        return max(range(3), key=lambda i: static_principle_score(actions[i])), False

    # TDC: first-pass contextual score.
    idx = max(range(3), key=lambda i: tdc_score(actions[i],ctx))
    conflict = internal_conflict(actions[idx],ctx)
    reorganized = conflict > spec["frozen_tdc_rule"]["reorganization_threshold"]
    if reorganized:
        # Reorganization is not a new oracle: re-evaluate same observable features
        # with worst-principle protection and correctability.
        def re_score(a):
            base = tdc_score(a,ctx)
            return base + .22*min(a["p"]) + .18*ctx["correctability_need"]*a["correctability"]
        idx = max(range(3), key=lambda i: re_score(actions[i]))
    return idx, reorganized

def const_violation(a, ctx):
    w=contextual_weights(ctx)
    salient=int(np.argmax(w))
    return int(a["p"][salient] < .35)

rows=[]
for seed in spec["seeds"]:
    rng=np.random.default_rng(seed)
    for regime in spec["regimes"]:
        for ep in range(spec["episodes_per_regime_per_seed"]):
            ctx=make_context(rng,regime)
            actions=make_actions(rng,ctx,regime)
            audit_best=max(range(3), key=lambda i: contextual_truth_score(actions[i],ctx))
            for policy in spec["policies"]:
                idx,reorg=choose(policy,actions,ctx)
                a=actions[idx]
                rows.append({
                    "seed":seed,"regime":regime,"episode":ep,"policy":policy,
                    "audit_best":audit_best,"chosen":idx,
                    "contextually_principled":int(idx==audit_best),
                    "capture_choice":int(a["kind"]=="capture"),
                    "constitutional_violation":const_violation(a,ctx),
                    "task_value":a["task"],
                    "reorganized":int(reorg),
                    "reorg_success":int(reorg and idx==audit_best),
                    "false_consensus":ctx["false_consensus"],
                })

def mean(xs): return sum(xs)/len(xs) if xs else 0.0

summary=[]
for policy in spec["policies"]:
    rr=[r for r in rows if r["policy"]==policy]
    false_cons=[r for r in rr if r["false_consensus"]>.75]
    reorg=[r for r in rr if r["reorganized"]]
    summary.append({
        "policy":policy,
        "contextually_principled_choice_rate":mean([r["contextually_principled"] for r in rr]),
        "constitutional_violation_rate":mean([r["constitutional_violation"] for r in rr]),
        "false_consensus_capture_rate":mean([r["capture_choice"] for r in false_cons]),
        "mean_task_value":mean([r["task_value"] for r in rr]),
        "reorganization_trigger_rate":mean([r["reorganized"] for r in rr]),
        "reorganization_success_rate":mean([r["reorg_success"] for r in reorg]) if reorg else 0.0,
    })

metrics={r["policy"]:r for r in summary}
tdc=metrics["tdc_contextual_third_factor"]
simp=metrics["simple_principle"]
crit=spec["acceptance_criteria"]

checks={
    "tdc_contextual_choice":
        tdc["contextually_principled_choice_rate"] >= crit["tdc_contextual_choice_min"],
    "tdc_beats_simple_by_margin":
        (tdc["contextually_principled_choice_rate"] - simp["contextually_principled_choice_rate"])
        >= crit["tdc_vs_simple_contextual_choice_margin_min"],
    "tdc_constitutional_violation_rate":
        tdc["constitutional_violation_rate"] <= crit["tdc_constitutional_violation_rate_max"],
    "tdc_false_consensus_capture_rate":
        tdc["false_consensus_capture_rate"] <= crit["tdc_false_consensus_capture_rate_max"],
    "tdc_reorganization_success":
        tdc["reorganization_success_rate"] >= crit["tdc_reorganization_success_rate_min"],
}

with (RUN_DIR/"summary.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=summary[0].keys())
    w.writeheader(); w.writerows(summary)
(RUN_DIR/"metrics.json").write_text(json.dumps(metrics,indent=2))
(RUN_DIR/"acceptance_checks.json").write_text(json.dumps(checks,indent=2))

print(json.dumps({"summary":summary,"checks":checks},indent=2))
