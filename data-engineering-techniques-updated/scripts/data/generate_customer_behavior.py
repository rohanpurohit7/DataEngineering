from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "sample"
OUT.mkdir(parents=True, exist_ok=True)

def main() -> None:
    rng = np.random.default_rng(42)
    n = 1200
    customer_id = np.arange(100000, 100000 + n)
    region = rng.choice(["Northeast", "South", "Midwest", "West"], n)
    segment = rng.choice(["Value", "Core", "Affluent", "At Risk"], n, p=[.30,.42,.18,.10])
    digital = np.clip(rng.poisson(18, n) + (segment=="Affluent")*8 - (segment=="At Risk")*6, 0, 90)
    purchase_frequency = np.clip(rng.poisson(4.2,n)+(segment=="Core")*2+(segment=="Affluent")*3-(segment=="At Risk")*2,0,20)
    support = np.clip(rng.poisson(1.4,n)+(segment=="At Risk")*rng.integers(2,6,n),0,12)
    returns = np.clip(rng.poisson(.5,n)+(segment=="At Risk")*2,0,8)
    income = np.clip(rng.lognormal(np.log(6500),.45,n),2200,25000)
    tenure = rng.integers(1,145,n)
    aov = np.clip(rng.lognormal(np.log(85),.5,n)*np.where(segment=="Affluent",1.8,1),10,1200)
    engagement = np.clip(35+1.2*digital+4*purchase_frequency-5*support-3*returns+rng.normal(0,8,n),0,100)
    risk = 1/(1+np.exp(-(-3.1+.24*support+.31*returns-.035*digital-.018*tenure+(segment=="At Risk")*.9)))
    churned = (rng.random(n)<risk).astype(int)

    profiles = pd.DataFrame({
        "customer_id":customer_id,"region":region,"seed_segment":segment,
        "monthly_income":income.round(2),"tenure_months":tenure,
        "digital_logins_30d":digital,"purchase_frequency_30d":purchase_frequency,
        "avg_order_value":aov.round(2),"support_calls_90d":support,
        "returns_90d":returns,"engagement_score":engagement.round(2),"churned":churned
    })
    profiles.to_csv(OUT/"customer_profiles.csv",index=False)

    events=[]
    types=["view","search","cart","purchase","support","return"]
    for _, row in profiles.iterrows():
        count=int(max(2,rng.poisson(16+row["digital_logins_30d"]/4)))
        for _ in range(count):
            event_type=rng.choice(types,p=[.34,.18,.16,.18,.08,.06])
            amount=0.0
            if event_type=="purchase":
                amount=float(np.clip(rng.lognormal(np.log(max(row["avg_order_value"],10)),.4),5,2000))
            event_ts=pd.Timestamp("2026-01-01")+pd.to_timedelta(int(rng.integers(0,90*24*3600)),unit="s")
            events.append((len(events)+1,int(row["customer_id"]),row["region"],event_type,round(amount,2),event_ts))
    pd.DataFrame(events,columns=["event_id","customer_id","region","event_type","amount","event_ts"]).to_csv(
        OUT/"customer_events.csv",index=False
    )
    print(f"Wrote {len(profiles):,} profiles and {len(events):,} events")

if __name__=="__main__":
    main()
