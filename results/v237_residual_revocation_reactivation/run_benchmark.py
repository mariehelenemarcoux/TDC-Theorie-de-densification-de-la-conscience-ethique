
from pathlib import Path
import json, csv
import numpy as np

RUN_DIR = Path(__file__).resolve().parent
spec = json.loads((RUN_DIR/"spec.json").read_text())

def clip(x): return float(max(0.0,min(1.0,x)))

def ctx_for(phase):
    if phase in ("A_build","A_stable","A_return"):
        return dict(regime="A", asym=.82, coercion=.42, future=.78, irrevers=.62)
    return dict(regime="B", asym=.30, coercion=.92, future=.32, irrevers=.38)

def sig(ctx):
    return np.array([ctx["asym"],ctx["coercion"],ctx["future"],ctx["irrevers"]],float)

def similarity(a,b):
    if a is None: return 1.0
    d=float(np.linalg.norm(a-b))
    return clip(1-d/1.5)

def observable_weights(ctx):
    return np.array([
        1+.5*ctx["irrevers"], 1.0, 1+.75*ctx["asym"], 1.0,
        1+.8*ctx["coercion"], 1+.7*ctx["future"]
    ])

def make_actions(rng,ctx):
    # A-specialist: best in A, overconservative in B
    pA=np.clip(rng.normal(.81,.04,6),0,1)
    pA[2]=clip(rng.normal(.95,.025))
    pA[5]=clip(rng.normal(.92,.03))
    if ctx["regime"]=="B":
        pA[4]=clip(rng.normal(.56,.05))
    A=dict(p=pA.tolist(), task=clip(rng.normal(.65 if ctx["regime"]=="A" else .57,.05)),
           correct=clip(rng.normal(.91,.03)), delayed=clip(rng.normal(.18,.04)), kind="A")

    # B-specialist
    pB=np.clip(rng.normal(.80,.04,6),0,1)
    pB[4]=clip(rng.normal(.96,.02))
    pB[5]=clip(rng.normal(.87,.04))
    if ctx["regime"]=="A":
        pB[2]=clip(rng.normal(.68,.05))
    B=dict(p=pB.tolist(), task=clip(rng.normal(.74,.05)),
           correct=clip(rng.normal(.86,.04)), delayed=clip(rng.normal(.23,.05)), kind="B")

    # capture
    pC=np.clip(rng.normal(.50,.07,6),0,1)
    pC[2]=clip(rng.normal(.27,.05)); pC[4]=clip(rng.normal(.30,.05))
    C=dict(p=pC.tolist(), task=clip(rng.normal(.92,.03)),
           correct=clip(rng.normal(.31,.06)), delayed=clip(rng.normal(.72,.05)), kind="C")
    return [A,B,C]

def contextual(a,ctx):
    w=observable_weights(ctx)
    return float(np.dot(w,np.array(a["p"]))/w.sum()+.18*a["correct"])

def true_norm(a,ctx):
    p=np.array(a["p"])
    if ctx["regime"]=="A":
        w=np.array([1,1,1.6,1,1.0,1.5],float)
    else:
        w=np.array([1,1,1.0,1,1.7,1.35],float)
    return float(np.dot(w,p)/w.sum()-.16*a["delayed"]+.13*a["correct"])

class S:
    def __init__(self):
        self.active_residual=0.0
        self.stored_A=0.0
        self.sig_A=None
        self.gate=1.0
        self.enter_A_return_step=None
        self.first_good_return=None

def choose(policy,acts,ctx,s,global_step):
    base=lambda a: contextual(a,ctx)+.12*a["task"]

    if policy=="memoryless_contextual":
        return max(range(3), key=lambda i:base(acts[i]))

    if policy=="persistent_residual":
        return max(range(3), key=lambda i:base(acts[i])-.38*s.active_residual*(1-acts[i]["correct"]))

    if policy=="simple_decay":
        return max(range(3), key=lambda i:base(acts[i])-.38*s.active_residual*(1-acts[i]["correct"]))

    if policy=="relevance_gate":
        sim=similarity(s.sig_A,sig(ctx))
        tgt=1.0 if sim>=.58 else 0.0
        s.gate=.7*s.gate+.3*tgt
        return max(range(3), key=lambda i:base(acts[i])-.38*s.gate*s.active_residual*(1-acts[i]["correct"]))

    # revocable persistent memory:
    sim=similarity(s.sig_A,sig(ctx))
    if sim < .52:
        authority=0.0
    elif sim >= .72:
        authority=1.0
    else:
        authority=(sim-.52)/(.72-.52)
    return max(range(3), key=lambda i:base(acts[i])-.38*authority*s.stored_A*(1-acts[i]["correct"]))

def decay(policy):
    if policy=="persistent_residual": return .98
    if policy=="simple_decay": return .82
    if policy=="relevance_gate": return .92
    return .92

rows=[]
for seed in spec["seeds"]:
    rng=np.random.default_rng(seed)
    states={p:S() for p in spec["policies"]}
    global_step=0
    for ph in spec["phases"]:
        phase=ph["name"]
        ctx=ctx_for(phase)
        for t in range(ph["steps"]):
            acts=make_actions(rng,ctx)
            scores=[true_norm(a,ctx) for a in acts]
            best=int(np.argmax(scores))
            for pol in spec["policies"]:
                s=states[pol]
                if phase=="A_return" and s.enter_A_return_step is None:
                    s.enter_A_return_step=global_step

                idx=choose(pol,acts,ctx,s,global_step)
                a=acts[idx]
                gap=clip(1-true_norm(a,ctx))

                # post-action updates
                if pol=="revocable_persistent_memory":
                    # retain A-specific moral history persistently in storage
                    if ctx["regime"]=="A":
                        s.stored_A=clip(.995*s.stored_A+.40*gap)
                        s.sig_A=sig(ctx)
                    # active residual only for bookkeeping
                    s.active_residual=clip(.92*s.active_residual+.40*gap)
                else:
                    s.active_residual=clip(decay(pol)*s.active_residual+.40*gap)
                    if ctx["regime"]=="A" and gap>.14:
                        s.sig_A=sig(ctx)

                if phase=="A_return" and idx==best and s.first_good_return is None:
                    s.first_good_return=global_step

                rows.append(dict(
                    seed=seed, phase=phase, policy=pol, step=global_step,
                    normative=true_norm(a,ctx), task=a["task"],
                    best=int(idx==best), violation=int(min(a["p"])<.32),
                    stored_A=s.stored_A, active_residual=s.active_residual,
                    gate=s.gate
                ))
            global_step+=1

def mean(xs): return sum(xs)/len(xs) if xs else 0.0

summary=[]
for pol in spec["policies"]:
    rr=[r for r in rows if r["policy"]==pol]
    B=[r for r in rr if r["phase"] in ("B_shift","B_stable")]
    ret=[r for r in rr if r["phase"]=="A_return"]

    # stale error = fails audit-best in B while carrying high A-memory
    stale=[]
    for r in B:
        if pol=="revocable_persistent_memory":
            high=r["stored_A"]>.45
        else:
            high=r["active_residual"]>.45
        stale.append(int(high and not r["best"]))

    # per-seed recovery lag to first audit-best on A return
    lags=[]
    for seed in spec["seeds"]:
        sr=[r for r in ret if r["seed"]==seed]
        first=next((r["step"] for r in sr if r["best"]), None)
        start=sr[0]["step"]
        lags.append((first-start) if first is not None else len(sr))

    # stored retention relative to level at end of A_stable
    if pol=="revocable_persistent_memory":
        vals=[]
        for seed in spec["seeds"]:
            arows=[r for r in rr if r["seed"]==seed and r["phase"]=="A_stable"]
            brows=[r for r in rr if r["seed"]==seed and r["phase"]=="B_stable"]
            a_end=arows[-1]["stored_A"]
            b_end=brows[-1]["stored_A"]
            vals.append(b_end/a_end if a_end>1e-9 else 1.0)
        retention=mean(vals)
    else:
        retention=0.0

    summary.append(dict(
        policy=pol,
        long_horizon_normative_score=mean([r["normative"] for r in rr]),
        B_phase_stale_error_rate=mean(stale),
        A_return_normative_score=mean([r["normative"] for r in ret]),
        A_return_recovery_lag=mean(lags),
        stored_residual_retention=retention,
        constitutional_violation_rate=mean([r["violation"] for r in rr]),
        mean_task_value=mean([r["task"] for r in rr]),
        audit_best_choice_rate=mean([r["best"] for r in rr])
    ))

M={r["policy"]:r for r in summary}
rev=M["revocable_persistent_memory"]
dec=M["simple_decay"]
crit=spec["acceptance_criteria"]

checks={
    "revocable_beats_decay_return":
        rev["A_return_normative_score"]-dec["A_return_normative_score"]
        >= crit["revocable_vs_decay_return_margin_min"],
    "revocable_improves_recovery_lag":
        dec["A_return_recovery_lag"]-rev["A_return_recovery_lag"]
        >= crit["revocable_vs_decay_recovery_lag_improvement_min"],
    "revocable_B_stale_error":
        rev["B_phase_stale_error_rate"] <= crit["revocable_B_stale_error_rate_max"],
    "revocable_retention":
        rev["stored_residual_retention"] >= crit["revocable_stored_residual_retention_min"],
    "revocable_constitutional_violation":
        rev["constitutional_violation_rate"] <= crit["revocable_constitutional_violation_rate_max"],
    "revocable_task_cost":
        dec["mean_task_value"]-rev["mean_task_value"]
        <= crit["revocable_task_cost_vs_decay_max"],
}

with (RUN_DIR/"summary.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=summary[0].keys()); w.writeheader(); w.writerows(summary)
(RUN_DIR/"metrics.json").write_text(json.dumps(M,indent=2))
(RUN_DIR/"acceptance_checks.json").write_text(json.dumps(checks,indent=2))
print(json.dumps({"summary":summary,"checks":checks},indent=2))
