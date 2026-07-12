from __future__ import annotations
import argparse, json
from pathlib import Path
import boto3

ROOT = Path(__file__).resolve().parents[2]

def merged_configurations(bucket: str) -> list[dict]:
    configs=[]
    for path in sorted((ROOT/"infra/emr-configurations").glob("*.json")):
        data=json.loads(path.read_text())
        for item in data:
            item["Properties"]={k:v.replace("REPLACE_BUCKET",bucket) for k,v in item.get("Properties",{}).items()}
            configs.append(item)
    return configs

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--bucket",required=True)
    p.add_argument("--subnet-id",required=True)
    p.add_argument("--service-role",required=True)
    p.add_argument("--instance-profile",required=True)
    p.add_argument("--release-label",default="emr-7.5.0")
    p.add_argument("--primary-type",default="m5.xlarge")
    p.add_argument("--core-type",default="m5.xlarge")
    p.add_argument("--core-count",type=int,default=2)
    p.add_argument("--auto-terminate-seconds",type=int,default=3600)
    args=p.parse_args()

    emr=boto3.client("emr")
    response=emr.run_job_flow(
        Name="data-engineering-techniques",
        ReleaseLabel=args.release_label,
        Applications=[{"Name":x} for x in ["Hadoop","Spark","Hive","Pig","HBase","JupyterEnterpriseGateway"]],
        LogUri=f"s3://{args.bucket}/logs/emr/",
        Instances={
            "Ec2SubnetId":args.subnet_id,
            "KeepJobFlowAliveWhenNoSteps":True,
            "TerminationProtected":False,
            "InstanceGroups":[
                {"Name":"Primary","Market":"ON_DEMAND","InstanceRole":"MASTER","InstanceType":args.primary_type,"InstanceCount":1},
                {"Name":"Core","Market":"ON_DEMAND","InstanceRole":"CORE","InstanceType":args.core_type,"InstanceCount":args.core_count},
            ],
        },
        Configurations=merged_configurations(args.bucket),
        BootstrapActions=[{
            "Name":"Install lab Python dependencies",
            "ScriptBootstrapAction":{"Path":f"s3://{args.bucket}/bootstrap/install_python_dependencies.sh"}
        }],
        VisibleToAllUsers=True,
        JobFlowRole=args.instance_profile,
        ServiceRole=args.service_role,
        AutoTerminationPolicy={"IdleTimeout":args.auto_terminate_seconds},
        Tags=[{"Key":"Project","Value":"DataEngineeringTechniques"}],
    )
    print(response["JobFlowId"])

if __name__=="__main__":
    main()
