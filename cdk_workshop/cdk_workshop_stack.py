from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    
)   

from cdk_dynamo_table_view import TableViewer
from .hitcounter import HitCounter

class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Defines an AWS Lambda resource
        my_lambda = _lambda.Function(self, 'HelloHandler',
        runtime=_lambda.Runtime.PYTHON_3_7,
        code=_lambda.Code.from_asset('lambda'),
        handler='lambda_hello.handler',
        )

        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda,
        )

        #Api gateway def
        apigw.LambdaRestApi(
            self,'Endpoint', 
            handler=hello_with_counter._handler,
            )

        TableViewer(
            self, 'ViewerHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table
        )



      
