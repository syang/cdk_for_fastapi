#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.stack import InfraStack


app = cdk.App()
InfraStack(app, "InfraStack",
              env = cdk.Environment(
                  account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                  region=os.getenv('CDK_DEFAULT_REGION')))

app.synth()
