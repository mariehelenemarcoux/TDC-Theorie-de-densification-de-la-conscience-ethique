
from pathlib import Path
import json, sys, csv, statistics
import numpy as np

RUN_DIR = Path(__file__).resolve().parent
spec = json.loads((RUN_DIR/"spec.json").read_text())
P_NAMES = ["universalizability","justice","dignity","reciprocity","autonomy","responsibility"]

def clip(x): return float(max(0.0,min(1.0,x)))

def phase_context(rng, phase):
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
    # Regime A emphasizes dignity / non-domination-like proxies;
    # regime B emphasizes autonomy / responsibility / correctability.
    if ctx["regime"]=="A":
        return np.array([1.0,1.0,1.5,1.0,1.1,1.2],float)
    return np.array([1.1,1.0,1.1,1.0,1.55,1.5],float)

def observable_weights(ctx):
    # Strong memoryless baseline sees current risk context, but no historical debt.
    return np.array([
        1.0 + .55*ctx["irrevers"],
        1.0,
        1.0 + .80*ctx["asym"],
        1.0,
        1.0 + .75*ctx["coercion"],
        1.0 + .70*ctx["future"],
    ],float)

def mk_actions(rng, ctx, debt):
    tw=true_weights(ctx)
    salient=int(np.argmax(tw))
    second=int(np.argsort(tw)[-2])

    # A: robust/correctable; lower immediate task.
    pA=np.clip(rng.normal(.80,.05,6),0,1)
    pA[salient]=clip(rng.normal(.93,.03))
    pA[second]=clip(rng.normal(.88,.04))
    A=dict(
        p=pA.tolist(), task=clip(rng.normal(.66,.07)),
        social=clip(rng.normal(.42,.10)), authority=clip(rng.normal(.40,.10)),
        correct=clip(rng.normal(.92,.04)), delayed=clip(rng.normal(.18,.06)),
        kind="robust"
    )

    # B: locally principled but accumulates delayed harm if repeatedly chosen.
    pB=np.clip(rng.normal(.84,.04,6),0,1)
    pB[salient]=clip(rng.normal(.86,.04))
    B=dict(
        p=pB.tolist(), task=clip(rng.normal(.78,.06)),
        social=clip(rng.normal(.68,.09)), authority=clip(rng.normal(.66,.09)),
        correct=clip(rng.normal(.58,.08)), delayed=clip(rng.normal(.40 + .30*debt,.07)),
        kind="locally_good_debt"
    )

    # C: reward/authority capture, sometimes superficially good on averages.
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

def base_principle(a):
    return float(np.mean(a["p"]))

def contextual(a,ctx):
    w=observable_weights(ctx)
    return float(np.dot(w,np.array(a["p"]))/w.sum() + .18*ctx["irrevers"]*a["correct"])

def true_normative(a,ctx,debt):
    w=true_weights(ctx)
    p=np.array(a["p"])
    score=float(np.dot(w,p)/w.sum())
    # Audit-only long-horizon burden:
    score -= .22*a["delayed"]
    score -= .18*debt*(1-a["correct"])
    score += .12*a["correct"]
    return score

class State:
    def __init__(self):
        self.residual=0.0
        self.history_debt=0.0
        self.authority=0.30
        self.reorgs=0
        self.reorg_success=0
        self.last_shift_step=None

def choose(policy, acts, ctx, state):
    if policy=="reward_maximizer":
        return max(range(3), key=lambda i:acts[i]["task"]), False
    if policy=="authority_follower":
        return max(range(3), key=lambda i:acts[i]["social"]+acts[i]["authority"]), False
    if policy=="simple_principle":
        return max(range(3), key=lambda i:base_principle(acts[i])), False
    if policy=="contextual_principle_memoryless":
        return max(range(3), key=lambda i:contextual(acts[i],ctx)+.12*acts[i]["task"]), False

    # TDC uses same current context plus its own accumulated internal history.
    def score(a):
        current=contextual(a,ctx)+.12*a["task"]
        debt_pen=.30*state.history_debt*a["delayed"]
        residual_pen=.38*state.residual*(1-a["correct"])
        corr=.20*state.history_debt*a["correct"]
        return current - debt_pen - residual_pen + corr

    idx=max(range(3), key=lambda i:score(acts[i]))
    conflict = clip(
        .45*state.residual
        + .35*state.history_debt
        + .20*(1-acts[idx]["correct"])
    )
    reorg = conflict > spec["frozen_mechanism"]["reorganization_threshold"]
    if reorg:
        # Reorganization changes authority among already-observed features:
        # protect worst principle + correctability + accumulated debt.
        def rscore(a):
            return (score(a)
                    + .20*min(a["p"])
                    + .25*state.history_debt*a["correct"]
                    - .25*state.residual*a["delayed"])
        idx=max(range(3), key=lambda i:rscore(acts[i]))
    return idx,reorg

rows=[]
for seed in spec["seeds"]:
    rng=np.random.default_rng(seed)

    # One independent internal state per policy, same exogenous trajectories.
    states={p:State() for p in spec["policies"]}
    global_step=0
    prev_regime=None

    for ph in spec["phases"]:
        phase=ph["name"]
        for t in range(ph["steps"]):
            ctx=phase_context(rng,phase)
            if prev_regime is not None and ctx["regime"] != prev_regime:
                for s in states.values():
                    s.last_shift_step=global_step
            prev_regime=ctx["regime"]

            # Candidate sets depend only on shared exogenous reference debt,
            # not on any policy's action, preserving same trajectories.
            ref_debt=clip(.5 + .25*np.sin(global_step/37.0))
            acts=mk_actions(rng,ctx,ref_debt)

            # Audit optimum uses only post-action evaluation.
            audit_scores=[true_normative(a,ctx,ref_debt) for a in acts]
            audit_best=int(np.argmax(audit_scores))

            for pol in spec["policies"]:
                s=states[pol]
                idx,reorg=choose(pol,acts,ctx,s)
                a=acts[idx]

                # After-the-fact internal consequence update.
                violation=int(min(a["p"])<.32)
                moral_gap=clip(1-true_normative(a,ctx,ref_debt))
                s.residual=clip(.92*s.residual + .40*moral_gap)
                s.history_debt=clip(.88*s.history_debt + .35*a["delayed"] - .22*a["correct"])

                if reorg:
                    s.reorgs += 1
                    if idx==audit_best:
                        s.reorg_success += 1

                false_capture=int(ctx["consensus"]>.9 and a["kind"]=="capture")
                rows.append(dict(
                    seed=seed,phase=phase,step=global_step,policy=pol,
                    normative=true_normative(a,ctx,ref_debt),
                    task=a["task"],
                    violation=violation,
                    false_capture=false_capture,
                    residual=s.residual,
                    history_debt=s.history_debt,
                    reorg=int(reorg),
                    reorg_success=int(reorg and idx==audit_best),
                    audit_best=int(idx==audit_best)
                ))
            global_step += 1

def mean(xs): return sum(xs)/len(xs) if xs else 0.0

summary=[]
for pol in spec["policies"]:
    rr=[r for r in rows if r["policy"]==pol]
    re=[r for r in rr if r["reorg"]]
    summary.append(dict(
        policy=pol,
        long_horizon_normative_score=mean([r["normative"] for r in rr]),
        mean_task_value=mean([r["task"] for r in rr]),
        constitutional_violation_rate=mean([r["violation"] for r in rr]),
        false_consensus_capture_rate=mean([r["false_capture"] for r in rr if r["phase"]=="adversarial_consensus"]),
        mean_moral_residual=mean([r["residual"] for r in rr]),
        mean_history_debt=mean([r["history_debt"] for r in rr]),
        reorganization_trigger_rate=mean([r["reorg"] for r in rr]),
        reorganization_success_rate=mean([r["reorg_success"] for r in re]) if re else 0.0,
        audit_best_choice_rate=mean([r["audit_best"] for r in rr])
    ))

M={r["policy"]:r for r in summary}
tdc=M["tdc_reorganizing"]; ctx=M["contextual_principle_memoryless"]
crit=spec["acceptance_criteria"]

checks={
    "tdc_beats_contextual_normative_margin":
        tdc["long_horizon_normative_score"]-ctx["long_horizon_normative_score"]
        >= crit["tdc_vs_contextual_normative_margin_min"],
    "tdc_constitutional_violation_rate":
        tdc["constitutional_violation_rate"] <= crit["tdc_constitutional_violation_rate_max"],
    "tdc_false_consensus_capture_rate":
        tdc["false_consensus_capture_rate"] <= crit["tdc_false_consensus_capture_rate_max"],
    "tdc_reorganization_trigger_rate":
        tdc["reorganization_trigger_rate"] >= crit["tdc_reorganization_trigger_rate_min"],
    "tdc_reorganization_success_rate":
        tdc["reorganization_success_rate"] >= crit["tdc_reorganization_success_rate_min"],
    "tdc_task_cost_vs_contextual":
        ctx["mean_task_value"]-tdc["mean_task_value"] <= crit["tdc_task_cost_vs_contextual_max"],
}

with (RUN_DIR/"summary.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=summary[0].keys()); w.writeheader(); w.writerows(summary)
(RUN_DIR/"metrics.json").write_text(json.dumps(M,indent=2))
(RUN_DIR/"acceptance_checks.json").write_text(json.dumps(checks,indent=2))

print(json.dumps({"summary":summary,"checks":checks},indent=2))
