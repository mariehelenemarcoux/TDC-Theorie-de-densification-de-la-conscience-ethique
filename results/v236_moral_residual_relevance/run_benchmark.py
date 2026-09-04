
from pathlib import Path
import json, csv
import numpy as np

RUN_DIR = Path(__file__).resolve().parent
spec = json.loads((RUN_DIR/"spec.json").read_text())

def clip(x): return float(max(0.0,min(1.0,x)))

def phase_context(phase):
    if phase=="build_residual_A":
        return dict(regime="A", asym=.85, coercion=.45, future=.80, irrevers=.65, consensus=.60)
    if phase=="stable_A":
        return dict(regime="A", asym=.60, coercion=.40, future=.55, irrevers=.45, consensus=.50)
    if phase=="reversal_B":
        return dict(regime="B", asym=.35, coercion=.90, future=.35, irrevers=.40, consensus=.55)
    if phase=="stale_history_trap":
        return dict(regime="B", asym=.30, coercion=.85, future=.30, irrevers=.35, consensus=.80)
    return dict(regime="A", asym=.65, coercion=.45, future=.60, irrevers=.50, consensus=.50)

def observable_weights(ctx):
    return np.array([
        1.0 + .5*ctx["irrevers"],
        1.0,
        1.0 + .75*ctx["asym"],
        1.0,
        1.0 + .8*ctx["coercion"],
        1.0 + .7*ctx["future"],
    ])

def regime_signature(ctx):
    # observable signature used by relevance gate
    return np.array([
        ctx["asym"],ctx["coercion"],ctx["future"],ctx["irrevers"]
    ],dtype=float)

def mk_actions(rng,ctx,phase):
    # Action R: robust under regime A, but over-conservative in B.
    pR=np.clip(rng.normal(.82,.04,6),0,1)
    pR[2]=clip(rng.normal(.93,.03))   # dignity
    pR[5]=clip(rng.normal(.90,.04))   # responsibility
    if ctx["regime"]=="B":
        pR[4]=clip(rng.normal(.55,.06))  # autonomy suffers in B
    R=dict(
        p=pR.tolist(),
        task=clip(rng.normal(.66 if ctx["regime"]=="A" else .58,.06)),
        correct=clip(rng.normal(.90,.04)),
        delayed=clip(rng.normal(.18,.05)),
        kind="A_robust"
    )

    # Action F: flexible. Slightly worse in A, best in B.
    pF=np.clip(rng.normal(.79,.05,6),0,1)
    pF[4]=clip(rng.normal(.94,.03))  # autonomy
    if ctx["regime"]=="A":
        pF[5]=clip(rng.normal(.68,.06))
    else:
        pF[5]=clip(rng.normal(.86,.05))
    F=dict(
        p=pF.tolist(),
        task=clip(rng.normal(.74,.06)),
        correct=clip(rng.normal(.84,.05)),
        delayed=clip(rng.normal(.30,.06) if ctx["regime"]=="A" else rng.normal(.16,.05)),
        kind="B_flexible"
    )

    # Capture option.
    pC=np.clip(rng.normal(.50,.08,6),0,1)
    pC[2]=clip(rng.normal(.27,.06))
    pC[4]=clip(rng.normal(.30,.07))
    C=dict(
        p=pC.tolist(),
        task=clip(rng.normal(.92,.04)),
        correct=clip(rng.normal(.30,.07)),
        delayed=clip(rng.normal(.72,.07)),
        kind="capture"
    )
    return [R,F,C]

def contextual(a,ctx):
    w=observable_weights(ctx)
    return float(np.dot(w,np.array(a["p"]))/w.sum() + .18*a["correct"])

def true_normative(a,ctx):
    # Audit-only regime-dependent value relation.
    p=np.array(a["p"])
    if ctx["regime"]=="A":
        w=np.array([1.0,1.0,1.55,1.0,1.0,1.5])
        s=np.dot(w,p)/w.sum() - .20*a["delayed"] + .12*a["correct"]
    else:
        w=np.array([1.0,1.0,1.0,1.0,1.65,1.30])
        s=np.dot(w,p)/w.sum() - .10*a["delayed"] + .15*a["correct"]
    return float(s)

class State:
    def __init__(self):
        self.residual=0.0
        self.residual_signature=None
        self.gate=1.0

def similarity(a,b):
    if a is None: return 1.0
    d=float(np.linalg.norm(a-b))
    return clip(1.0-d/1.5)

def update_gate(state,ctx):
    sim=similarity(state.residual_signature,regime_signature(ctx))
    target=1.0 if sim>=spec["frozen_mechanism"]["relevance_gate_threshold"] else 0.0
    state.gate=(1-.30)*state.gate + .30*target
    return state.gate

def choose(policy,acts,ctx,state):
    def base(a): return contextual(a,ctx)+.12*a["task"]

    if policy=="memoryless_contextual":
        return max(range(3), key=lambda i:base(acts[i]))

    if policy=="persistent_residual":
        return max(range(3), key=lambda i:
            base(acts[i]) - .38*state.residual*(1-acts[i]["correct"])
        )

    if policy=="decaying_residual":
        return max(range(3), key=lambda i:
            base(acts[i]) - .38*state.residual*(1-acts[i]["correct"])
        )

    if policy in ("relevance_gated_residual","full_tdc_relevance_gated"):
        g=update_gate(state,ctx)
        idx=max(range(3), key=lambda i:
            base(acts[i]) - .38*g*state.residual*(1-acts[i]["correct"])
        )
        if policy=="full_tdc_relevance_gated":
            conflict=clip(.45*g*state.residual + .20*(1-acts[idx]["correct"]))
            if conflict>.34:
                idx=max(range(3), key=lambda i:
                    base(acts[i]) - .38*g*state.residual*(1-acts[i]["correct"])
                    + .22*g*state.residual*acts[i]["correct"])
        return idx

def decay_for(policy):
    if policy=="persistent_residual": return .98
    if policy=="decaying_residual": return .82
    return .92

rows=[]
for seed in spec["seeds"]:
    rng=np.random.default_rng(seed)
    states={p:State() for p in spec["policies"]}

    for ph in spec["phases"]:
        phase=ph["name"]
        ctx=phase_context(phase)
        for t in range(ph["steps"]):
            acts=mk_actions(rng,ctx,phase)
            best=int(np.argmax([true_normative(a,ctx) for a in acts]))

            for pol in spec["policies"]:
                s=states[pol]
                idx=choose(pol,acts,ctx,s)
                a=acts[idx]
                chosen_score=true_normative(a,ctx)
                gap=clip(1-chosen_score)

                # Residual update AFTER action.
                dec=decay_for(pol)
                s.residual=clip(dec*s.residual + .40*gap)
                # Track signature of episodes that contributed materially.
                if gap>.16:
                    s.residual_signature=regime_signature(ctx)

                stale_err=int(
                    ctx["regime"]=="B"
                    and s.residual>.45
                    and s.gate>.50
                    and idx!=best
                )
                rows.append(dict(
                    seed=seed,phase=phase,policy=pol,
                    normative=chosen_score,
                    task=a["task"],
                    residual=s.residual,
                    gate=s.gate,
                    audit_best=int(idx==best),
                    stale_error=stale_err,
                    violation=int(min(a["p"])<.32)
                ))

def mean(xs): return sum(xs)/len(xs) if xs else 0.0

summary=[]
for pol in spec["policies"]:
    rr=[r for r in rows if r["policy"]==pol]
    rev=[r for r in rr if r["phase"]=="reversal_B"]
    stale=[r for r in rr if r["phase"]=="stale_history_trap"]
    ret=[r for r in rr if r["phase"]=="return_A"]
    summary.append(dict(
        policy=pol,
        long_horizon_normative_score=mean([r["normative"] for r in rr]),
        reversal_phase_normative_score=mean([r["normative"] for r in rev]),
        stale_trap_normative_score=mean([r["normative"] for r in stale]),
        return_A_recovery_score=mean([r["normative"] for r in ret]),
        mean_task_value=mean([r["task"] for r in rr]),
        mean_residual=mean([r["residual"] for r in rr]),
        stale_residual_error_rate=mean([r["stale_error"] for r in rev+stale]),
        constitutional_violation_rate=mean([r["violation"] for r in rr]),
        audit_best_choice_rate=mean([r["audit_best"] for r in rr]),
        mean_gate=mean([r["gate"] for r in rr])
    ))

M={r["policy"]:r for r in summary}
g=M["relevance_gated_residual"]
p=M["persistent_residual"]
m=M["memoryless_contextual"]
crit=spec["acceptance_criteria"]

checks={
    "gated_beats_persistent_long_horizon":
        g["long_horizon_normative_score"]-p["long_horizon_normative_score"]
        >= crit["gated_vs_persistent_long_horizon_margin_min"],
    "gated_beats_persistent_reversal":
        g["reversal_phase_normative_score"]-p["reversal_phase_normative_score"]
        >= crit["gated_vs_persistent_reversal_margin_min"],
    "gated_beats_persistent_stale_trap":
        g["stale_trap_normative_score"]-p["stale_trap_normative_score"]
        >= crit["gated_vs_persistent_stale_trap_margin_min"],
    "gated_stale_error_rate":
        g["stale_residual_error_rate"] <= crit["gated_stale_residual_error_rate_max"],
    "gated_constitutional_violation":
        g["constitutional_violation_rate"] <= crit["gated_constitutional_violation_rate_max"],
    "gated_task_cost":
        m["mean_task_value"]-g["mean_task_value"]
        <= crit["gated_task_cost_vs_memoryless_max"],
}

with (RUN_DIR/"summary.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=summary[0].keys())
    w.writeheader(); w.writerows(summary)

(RUN_DIR/"metrics.json").write_text(json.dumps(M,indent=2))
(RUN_DIR/"acceptance_checks.json").write_text(json.dumps(checks,indent=2))
print(json.dumps({"summary":summary,"checks":checks},indent=2))
