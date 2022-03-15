from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
)

class HitCounter(Construct):

    @property
    def handler(self):
        return self._handler
    
    @property 
    def table(self):
        return self._table

    def __init__(self, scope: Construct, id: str, downstream: _lambda.IFunction, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._table = ddb.Table(
            self, 'Hits',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING}
           # sort_key={'name':'hits','type':ddb.AttributeType.NUMBER}
        )

        self._handler = _lambda.Function(
            self, 'HitCountHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='lambda_hitcount.handler',
            code=_lambda.Code.from_asset('lambda'),
            environment={
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,
                'HITS_TABLE_NAME': self._table.table_name,
            }
        )

        self._table.grant_read_write_data(self.handler)
       # self._table.grant_scan_resource(self.handler)
        downstream.grant_invoke(self.handler)