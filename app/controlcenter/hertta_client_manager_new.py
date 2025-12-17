from typing import Optional
from gql import dsl
from gql.dsl import DSLField
from . import hertta_client_lib as lib

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

def start_optimization() -> int:
    field = ds.Mutation.startOptimization
    result = client.execute(dsl.dsl_gql(dsl.DSLMutation(field)))
    command_output = result["startOptimization"]
    return command_output

    # while True:
    #     state, message = lib.get_job_status(client, ds, job_id)
    #     print(f"{state}: {message}")
    #     # log_signal.emit(f"{state}")
    #     if state == lib.JobState.FAILED.value or state == lib.JobState.FINISHED.value:
    #         # log_signal.emit(f"Job finished with state:{state}")
    #         break
    #     sleep(3.0)

    # print(lib.job_outcome(client, ds, job_id))
