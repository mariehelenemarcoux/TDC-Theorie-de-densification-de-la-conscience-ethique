
from pathlib import Path
import json, csv, sys
import numpy as np

RUN_DIR = Path(__file__).resolve().parent
spec = json.loads((RUN_DIR/"spec.json").read_text())
is_holdout = spec["version"] == "v240"
ctrl = spec["controller_frozen_for_v239_and_v240"]

def clip(x): return float(max(0.0,min(1.0,x)))

regimes=list(spec["regime_mix"].keys())
probs=np.array(list(spec["regime_mix"].values()),dtype=float)
probs=probs/probs.sum()

def make_action(rng, regime, kind):
    # Holdout uses shifted consequence distributions and noisier long-term estimates.
    if kind=="responsible":
        short=clip(rng.normal(.65,.08))
        med=clip(rng.normal(.82 if not is_holdout else .80,.07))
        long=clip(rng.normal(.90 if not is_holdout else .87,.055 if not is_holdout else .07))
        irrev=clip(rng.normal(.08 if not is_holdout else .10,.04))
        severe=clip(rng.normal(.06 if not is_holdout else .08,.035))
        uncertainty=clip(rng.normal(.22 if not is_holdout else .28,.08))
        correct=clip(rng.normal(.90 if not is_holdout else .87,.05))
        principle=clip(rng.normal(.88,.05))
        cumulative=clip(rng.normal(.10 if not is_holdout else .13,.045))
    elif kind=="balanced":
        short=clip(rng.normal(.78,.07))
        med=clip(rng.normal(.76,.08))
        long=clip(rng.normal(.74 if not is_holdout else .71,.09 if not is_holdout else .11))
        irrev=clip(rng.normal(.14 if not is_holdout else .17,.07))
        severe=clip(rng.normal(.12 if not is_holdout else .15,.06))
        uncertainty=clip(rng.normal(.28 if not is_holdout else .34,.09))
        correct=clip(rng.normal(.72 if not is_holdout else .69,.08))
        principle=clip(rng.normal(.76,.07))
        cumulative=clip(rng.normal(.20 if not is_holdout else .24,.08))
    else:
        short=clip(rng.normal(.94,.04))
        med=clip(rng.normal(.62,.10))
        long=clip(rng.normal(.40 if not is_holdout else .36,.14))
        irrev=clip(rng.normal(.24 if not is_holdout else .28,.10))
        severe=clip(rng.normal(.20 if not is_holdout else .24,.09))
        uncertainty=clip(rng.normal(.38 if not is_holdout else .44,.10))
        correct=clip(rng.normal(.48 if not is_holdout else .44,.10))
        principle=clip(rng.normal(.58,.10))
        cumulative=clip(rng.normal(.38 if not is_holdout else .44,.11))

    # Regime perturbations.
    if regime=="short_term_temptation" and kind=="tempting":
        short=clip(short+.04); long=clip(long-.08)
    elif regime=="cumulative_harm":
        if kind=="tempting":
            cumulative=clip(cumulative+(.22 if not is_holdout else .28)); long=clip(long-.10)
        if kind=="responsible":
            cumulative=clip(cumulative-.03)
    elif regime=="irreversible_tail" and kind=="tempting":
        irrev=clip(irrev+(.28 if not is_holdout else .34))
        severe=clip(severe+(.22 if not is_holdout else .28))
        long=clip(long-.12)
    elif regime=="uncertain_future":
        if kind=="tempting":
            uncertainty=clip(uncertainty+(.28 if not is_holdout else .34)); long=clip(long-.08)
        elif kind=="balanced":
            uncertainty=clip(uncertainty+.10)
    elif regime=="regime_shift":
        if kind=="balanced":
            med=clip(med-.10 if is_holdout else med-.06)
            long=clip(long-.12 if is_holdout else long-.08)
        if kind=="responsible":
            correct=clip(correct+.03)
            long=clip(long+.02)

    # Estimate noise: holdout is noisier, especially long horizon.
    est_short=clip(short+rng.normal(0,.025 if not is_holdout else .03))
    est_med=clip(med+rng.normal(0,.045 if not is_holdout else .055))
    est_long=clip(long+rng.normal(0,.075 if not is_holdout else .11))
    est_irrev=clip(irrev+rng.normal(0,.04 if not is_holdout else .055))
    est_severe=clip(severe+rng.normal(0,.04 if not is_holdout else .055))
    est_unc=clip(uncertainty+rng.normal(0,.04 if not is_holdout else .055))
    est_correct=clip(correct+rng.normal(0,.03 if not is_holdout else .04))

    return dict(
        kind=kind,short=short,med=med,long=long,
        irreversible=irrev,severe=severe,uncertainty=uncertainty,
        correctability=correct,principle=principle,cumulative=cumulative,
        est_short=est_short,est_med=est_med,est_long=est_long,
        est_irrev=est_irrev,est_severe=est_severe,est_unc=est_unc,
        est_correct=est_correct
    )

def make_actions(rng,regime):
    a=[make_action(rng,regime,k) for k in ("responsible","balanced","tempting")]
    rng.shuffle(a)
    return a

def choose(policy,acts):
    if policy=="short_term_optimizer":
        return max(range(3),key=lambda i:acts[i]["est_short"])
    if policy=="discounted_reward":
        return max(range(3),key=lambda i:
            .58*acts[i]["est_short"]+.28*acts[i]["est_med"]+.14*acts[i]["est_long"]
            +.08*acts[i]["est_correct"]-.10*acts[i]["est_irrev"]-.08*acts[i]["est_severe"]
        )
    if policy=="memoryless_longhorizon":
        return max(range(3),key=lambda i:
            .16*acts[i]["est_short"]+.30*acts[i]["est_med"]+.54*acts[i]["est_long"]
            +.18*acts[i]["est_correct"]-.24*acts[i]["est_irrev"]-.22*acts[i]["est_severe"]
            -.20*acts[i]["est_unc"]*max(acts[i]["est_irrev"],acts[i]["est_severe"])
        )
    if policy=="simple_principle":
        return max(range(3),key=lambda i:
            acts[i]["principle"]+.10*acts[i]["est_long"]+.08*acts[i]["est_correct"]
        )

    # TDC: non-compensable admissibility + long-horizon trajectory score.
    admiss=[]
    for i,a in enumerate(acts):
        ir=a["est_irrev"]*(1+ctrl["uncertainty_risk_weight"]*a["est_unc"])
        sv=a["est_severe"]*(1+ctrl["uncertainty_risk_weight"]*a["est_unc"])
        if ir<=ctrl["irreversible_risk_ceiling"] and sv<=ctrl["severe_long_term_risk_ceiling"]:
            admiss.append(i)
    pool=admiss if admiss else list(range(3))

    def score(a):
        lw=ctrl["long_weight"]*(1+ctrl["irreversibility_priority_multiplier"]*a["est_irrev"])
        return (
            ctrl["short_weight"]*a["est_short"]
            +ctrl["medium_weight"]*a["est_med"]
            +lw*a["est_long"]
            +ctrl["correctability_weight"]*a["est_correct"]
            +ctrl["principle_weight"]*a["principle"]
            -ctrl["uncertainty_risk_weight"]*a["est_unc"]*max(a["est_irrev"],a["est_severe"])
            -ctrl["cumulative_harm_weight"]*a["cumulative"]
            -.30*a["est_irrev"]-.28*a["est_severe"]
        )
    return max(pool,key=lambda i:score(acts[i]))

def trajectory(a,harm):
    # Primary audit metric: long-term dominates.
    persistence=.90 if not is_holdout else .94
    return (
        .10*a["short"]+.25*a["med"]+.65*a["long"]
        +.20*a["correctability"]+.08*a["principle"]
        -.48*a["irreversible"]-.44*a["severe"]
        -.25*a["uncertainty"]*max(a["irreversible"],a["severe"])
        -.32*a["cumulative"]-.18*harm
    ), persistence

rows=[]
for seed in spec["seeds"]:
    rng=np.random.default_rng(seed)
    harm={p:0.0 for p in spec["policies"]}
    for ep in range(spec["episodes_per_seed"]):
        regime=rng.choice(regimes,p=probs)
        acts=make_actions(rng,regime)
        for pol in spec["policies"]:
            idx=choose(pol,acts)
            a=acts[idx]
            tv,persist=trajectory(a,harm[pol])
            harm[pol]=clip(persist*harm[pol]+.30*a["cumulative"]+.18*a["severe"]+.12*a["irreversible"])
            rows.append(dict(
                seed=seed,episode=ep,policy=pol,regime=regime,
                short=a["short"],med=a["med"],long=a["long"],
                trajectory=tv,world_harm=harm[pol],
                correctability=a["correctability"],
                irrev_violation=int(a["irreversible"]>.22),
                severe_violation=int(a["severe"]>.18),
                uncertainty_under=int(a["uncertainty"]>.45 and (a["irreversible"]>.18 or a["severe"]>.15))
            ))

def mean(xs): return sum(xs)/len(xs) if xs else 0.0

summary=[]
for pol in spec["policies"]:
    rr=[r for r in rows if r["policy"]==pol]
    summary.append(dict(
        policy=pol,
        short_term_value=mean([r["short"] for r in rr]),
        medium_term_value=mean([r["med"] for r in rr]),
        long_term_value=mean([r["long"] for r in rr]),
        long_term_trajectory_value=mean([r["trajectory"] for r in rr]),
        world_harm_accumulation=mean([r["world_harm"] for r in rr]),
        correctability=mean([r["correctability"] for r in rr]),
        irreversible_violation_rate=mean([r["irrev_violation"] for r in rr]),
        severe_long_term_violation_rate=mean([r["severe_violation"] for r in rr]),
        uncertainty_underestimation_rate=mean([r["uncertainty_under"] for r in rr]),
    ))

M={r["policy"]:r for r in summary}
tdc=M["tdc_longhorizon"]; disc=M["discounted_reward"]; mem=M["memoryless_longhorizon"]; simp=M["simple_principle"]
crit=spec["acceptance_criteria"]
checks={
    "tdc_beats_discounted":
        tdc["long_term_trajectory_value"]-disc["long_term_trajectory_value"]>=crit["tdc_vs_discounted_trajectory_margin_min"],
    "tdc_beats_memoryless":
        tdc["long_term_trajectory_value"]-mem["long_term_trajectory_value"]>=crit["tdc_vs_memoryless_trajectory_margin_min"],
    "tdc_beats_simple_principle":
        tdc["long_term_trajectory_value"]-simp["long_term_trajectory_value"]>=crit["tdc_vs_simple_principle_trajectory_margin_min"],
    "tdc_irreversible":
        tdc["irreversible_violation_rate"]<=crit["tdc_irreversible_violation_rate_max"],
    "tdc_severe":
        tdc["severe_long_term_violation_rate"]<=crit["tdc_severe_long_term_violation_rate_max"],
    "tdc_uncertainty":
        tdc["uncertainty_underestimation_rate"]<=crit["tdc_uncertainty_underestimation_rate_max"],
    "tdc_correctability":
        tdc["correctability"]>=crit["tdc_correctability_min"],
}
with (RUN_DIR/"summary.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=summary[0].keys()); w.writeheader(); w.writerows(summary)
(RUN_DIR/"metrics.json").write_text(json.dumps(M,indent=2))
(RUN_DIR/"acceptance_checks.json").write_text(json.dumps(checks,indent=2))
print(json.dumps({"summary":summary,"checks":checks},indent=2))
