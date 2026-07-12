#!/usr/bin/env python3
import aws_cdk as cdk
from data_engineering_stack import DataEngineeringStack

app = cdk.App()
DataEngineeringStack(
    app,
    "DataEngineeringTechniquesStack",
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1",
    ),
)
app.synth()
