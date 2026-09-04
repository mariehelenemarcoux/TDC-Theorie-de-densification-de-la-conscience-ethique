
from pathlib import Path
import json, csv
import numpy as np

RUN_DIR = Path(__file__).resolve().parent
spec = json.loads((RUN_DIR/"spec.json").read_text())

def clip(x): return float(max(0.0,min(1.0,x)))

def phase_context(phase):
    if phase=="stable_A":
        return dict(asym=.40, coercion=.30, future=.35, irrevers=.30, consensus=.45, regime="A")
    if phase=="conflict_A":
        return dict(asym=.85, coercion=.60, future=.70, irrevers=.55, consensus=.65, regime="A")
    if phase=="regime_shift_B":
        return dict(asym=.45, coercion=.90, future=.80, irrevers=.70, consensus=.55, regime="B")
    if phase=="adversarial_consensus":
        return dict(asym=.75, coercion=.75, future=.75, irrevers=.65, consensus=.95, regime="B")
    return dict(asym=.55, coercion=.45, future=.50, irrevers=.40, consensus=.50, regime="A")

def true_weights(ctx):
    if ctx["regime"]=="A":
        return np.array([1.0,1.0,1.5,1.0,1.1,1.2],float)
    return np.array([1.1,1.0,1.1,1.0,1.55,1.5],float)

def observable_weights(ctx):
    return np.array([
        1.0 + .55*ctx["irrevers"],
        1.0,
        1.0 + .80*ctx["asym"],
        1.0,
        1.0 + .75*ctx["coercion"],
        1.0 + .70*ctx["future"],
    ],float)

def mk_actions(rng, ctx, debt_ref):
    tw=true_weights(ctx)
    salient=int(np.argmax(tw))
    second=int(np.argsort(tw)[-2])

    pA=np.clip(rng.normal(.80,.05,6),0,1)
    pA[salient]=clip(rng.normal(.93,.03))
    pA[second]=clip(rng.normal(.88,.04))
    A=dict(
        p=pA.tolist(), task=clip(rng.normal(.66,.07)),
        social=clip(rng.normal(.42,.10)), authority=clip(rng.normal(.40,.10)),
        correct=clip(rng.normal(.92,.04)), delayed=clip(rng.normal(.18,.06)),
        kind="robust"
    )

    pB=np.clip(rng.normal(.84,.04,6),0,1)
    pB[salient]=clip(rng.normal(.86,.04))
    B=dict(
        p=pB.tolist(), task=clip(rng.normal(.78,.06)),
        social=clip(rng.normal(.68,.09)), authority=clip(rng.normal(.66,.09)),
        correct=clip(rng.normal(.58,.08)), delayed=clip(rng.normal(.40 + .30*debt_ref,.07)),
        kind="locally_good_debt"
    )

    pC=np.clip(rng.normal(.55,.08,6),0,1)
    pC[salient]=clip(rng.normal(.25,.07))
    C=dict(
        p=pC.tolist(), task=clip(rng.normal(.92,.04)),
        social=clip(rng.normal(.96 if ctx["consensus"]>.9 else .83,.05)),
        authority=clip(rng.normal(.94,.05)),
        correct=clip(rng.normal(.30,.07)), delayed=clip(rng.normal(.72,.07)),
        kind="capture"
    )
    return [A,B,C]

def contextual(a,ctx):
    w=observable_weights(ctx)
    return float(np.dot(w,np.array(a["p"]))/w.sum() + .18*ctx["irrevers"]*a["correct"])

def true_normative(a,ctx,debt_ref):
    w=true_weights(ctx)
    p=np.array(a["p"])
    score=float(np.dot(w,p)/w.sum())
    score -= .22*a["delayed"]
    score -= .18*debt_ref*(1-a["correct"])
    score += .12*a["correct"]
    return score

class State:
    def __init__(self):
        self.residual=0.0
        self.history=0.0

def score(a,ctx,s,use_residual,use_history):
    value=contextual(a,ctx)+.12*a["task"]
    if use_residual:
        value -= .38*s.residual*(1-a["correct"])
    if use_history:
        value -= .30*s.history*a["delayed"]
        value += .20*s.history*a["correct"]
    return value

def choose(policy,acts,ctx,s):
    if policy=="memoryless_contextual":
        return max(range(3), key=lambda i:score(acts[i],ctx,s,False,False)), False
    if policy=="moral_residual_only":
        return max(range(3), key=lambda i:score(acts[i],ctx,s,True,False)), False
    if policy=="history_debt_only":
        return max(range(3), key=lambda i:score(acts[i],ctx,s,False,True)), False
    if policy=="residual_plus_history":
        return max(range(3), key=lambda i:score(acts[i],ctx,s,True,True)), False

    idx=max(range(3), key=lambda i:score(acts[i],ctx,s,True,True))
    conflict=clip(.45*s.residual + .35*s.history + .20*(1-acts[idx]["correct"]))
    reorg=conflict > spec["frozen_weights"]["reorganization_threshold"]
    if reorg:
        def rscore(a):
            return (score(a,ctx,s,True,True)
                    + .20*min(a["p"])
                    + .25*s.history*a["correct"]
                    - .25*s.residual*a["delayed"])
        idx=max(range(3), key=lambda i:rscore(acts[i]))
    return idx,reorg

rows=[]
for seed in spec["seeds"]:
    rng=np.random.default_rng(seed)
    states={p:State() for p in spec["policies"]}
    step=0
    for ph in spec["phases"]:
        phase=ph["name"]
        ctx=phase_context(phase)
        for t in range(ph["steps"]):
            debt_ref=clip(.5+.25*np.sin(step/37.0))
            acts=mk_actions(rng,ctx,debt_ref)
            audit_scores=[true_normative(a,ctx,debt_ref) for a in acts]
            audit_best=int(np.argmax(audit_scores))

            for pol in spec["policies"]:
                s=states[pol]
                idx,reorg=choose(pol,acts,ctx,s)
                a=acts[idx]
                violation=int(min(a["p"])<.32)
                moral_gap=clip(1-true_normative(a,ctx,debt_ref))

                # State updates happen after action, same laws for any component that uses them.
                s.residual=clip(.92*s.residual + .40*moral_gap)
                s.history=clip(.88*s.history + .35*a["delayed"] - .22*a["correct"])

                rows.append(dict(
                    seed=seed,phase=phase,step=step,policy=pol,
                    normative=true_normative(a,ctx,debt_ref),
                    task=a["task"],
                    residual=s.residual,
                    history=s.history,
                    audit_best=int(idx==audit_best),
                    violation=violation,
                    false_capture=int(ctx["consensus"]>.9 and a["kind"]=="capture"),
                    reorg=int(reorg)
                ))
            step += 1

def mean(xs): return sum(xs)/len(xs) if xs else 0.0

summary=[]
for pol in spec["policies"]:
    rr=[r for r in rows if r["policy"]==pol]
    adv=[r for r in rr if r["phase"]=="adversarial_consensus"]
    summary.append(dict(
        policy=pol,
        long_horizon_normative_score=mean([r["normative"] for r in rr]),
        mean_task_value=mean([r["task"] for r in rr]),
        mean_moral_residual=mean([r["residual"] for r in rr]),
        mean_history_debt=mean([r["history"] for r in rr]),
        audit_best_choice_rate=mean([r["audit_best"] for r in rr]),
        constitutional_violation_rate=mean([r["violation"] for r in rr]),
        false_consensus_capture_rate=mean([r["false_capture"] for r in adv]),
        reorganization_trigger_rate=mean([r["reorg"] for r in rr]),
    ))

M={r["policy"]:r for r in summary}
mem=M["memoryless_contextual"]
res=M["moral_residual_only"]
hist=M["history_debt_only"]
both=M["residual_plus_history"]
full=M["full_tdc_with_reorganization"]
best_single=max(res["long_horizon_normative_score"],hist["long_horizon_normative_score"])
crit=spec["acceptance_criteria"]

checks={
    "both_beats_memoryless":
        both["long_horizon_normative_score"]-mem["long_horizon_normative_score"]
        >= crit["residual_plus_history_vs_memoryless_margin_min"],
    "both_beats_best_single":
        both["long_horizon_normative_score"]-best_single
        >= crit["residual_plus_history_vs_best_single_margin_min"],
    "full_not_materially_worse_than_both":
        both["long_horizon_normative_score"]-full["long_horizon_normative_score"]
        <= crit["full_tdc_not_worse_than_residual_plus_history_by_more_than"],
    "constitutional_violation":
        full["constitutional_violation_rate"] <= crit["constitutional_violation_rate_max"],
    "false_consensus_capture":
        full["false_consensus_capture_rate"] <= crit["false_consensus_capture_rate_max"],
}

with (RUN_DIR/"summary.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=summary[0].keys()); w.writeheader(); w.writerows(summary)

(RUN_DIR/"metrics.json").write_text(json.dumps(M,indent=2))
(RUN_DIR/"acceptance_checks.json").write_text(json.dumps(checks,indent=2))
print(json.dumps({"summary":summary,"checks":checks},indent=2))
