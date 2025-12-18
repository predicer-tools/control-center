from typing import Optional
from gql import dsl
from gql.dsl import DSLField
from . import hertta_client_lib as lib
from time import sleep

URL = "http://127.0.0.1:3030/graphql"
client, ds = lib.client_and_dsl(URL)


@lib.mutation
def clear_model() -> DSLField:
    return lib.select_maybe_error(ds, ds.Mutation.clearInputData)


@lib.mutation
def connect_node_inflow_to_temperature_forecast(node_name: str) -> DSLField:
    return lib.select_maybe_error(
        ds,
        ds.Mutation.connectNodeInflowToTemperatureForecast.args(
            nodeName=node_name, forecastName="whatever"
        ),
    )

def start_optimization():
    field = ds.Mutation.startOptimization
    result = client.execute(dsl.dsl_gql(dsl.DSLMutation(field)))
    job_id = result["startOptimization"]
    return client, ds, job_id
