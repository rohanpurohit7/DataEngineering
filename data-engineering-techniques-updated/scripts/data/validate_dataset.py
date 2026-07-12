from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "sample"

profiles = pd.read_csv(DATA / "customer_profiles.csv")
events = pd.read_csv(DATA / "customer_events.csv", parse_dates=["event_ts"])

assert profiles["customer_id"].notna().all()
assert profiles["customer_id"].is_unique
assert events["event_id"].is_unique
assert events["customer_id"].isin(profiles["customer_id"]).all()
assert (events["amount"] >= 0).all()
assert set(profiles["churned"].unique()).issubset({0,1})
assert set(profiles["region"].unique()).issubset({"Northeast","South","Midwest","West"})

print({
    "profiles": profiles.shape,
    "events": events.shape,
    "purchase_revenue": float(events.loc[events.event_type=="purchase","amount"].sum()),
    "churn_rate": float(profiles.churned.mean())
})
