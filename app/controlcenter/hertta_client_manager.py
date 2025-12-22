from typing import Optional, Tuple
from time import sleep
from gql import dsl
from gql.dsl import DSLField
from . import hertta_client_lib as lib
from gql.transport.exceptions import TransportQueryError

URL = "http://127.0.0.1:3030/graphql"
client, ds = lib.client_and_dsl(URL)


@lib.mutation
def connect_market_prices_to_forecast(market_name: str) -> DSLField:
    return lib.select_maybe_error(
        ds,
        ds.Mutation.connectMarketPricesToForecast.args(
            marketName=market_name, forecastName="whatever"
        ),
    )

def set_location(country: str, place: str) -> tuple[bool, Optional[list]]:

    settings_fragment = dsl.DSLFragment("SettingsResultAsSettings")
    settings_fragment.on(ds.Settings)
    settings_fragment.select(
        ds.Settings.location.select(
            ds.LocationSettings.country,
            ds.LocationSettings.place,
        )
    )

    errors_fragment = dsl.DSLFragment("SettingsResultAsValidationErrors")
    errors_fragment.on(ds.ValidationErrors)
    errors_fragment.select(
        ds.ValidationErrors.errors.select(
            ds.ValidationError.field,
            ds.ValidationError.message,
        )
    )

    field = ds.Mutation.updateSettings.args(
        settingsInput={
            "location": {
                "country": country,
                "place": place,
            }
        }
    ).select(settings_fragment, errors_fragment)

    result = client.execute(
        dsl.dsl_gql(
            dsl.DSLMutation(field),
            settings_fragment,
            errors_fragment,
        )
    )

    payload = result["updateSettings"]
    if "errors" in payload:
        return False, payload["errors"]
    return True, payload.get("location")

def poll_job_until_finished(job_id: int, poll_interval: float = 2.0) -> dict:
    current_state = None

    while True:
        try:
            state, message = lib.get_job_status(client, ds, job_id)
        except TransportQueryError as e:
            print(f"[jobStatus] TransportQueryError for job {job_id}:", e.errors or e)
            return {}
        except Exception as e:
            print(f"[jobStatus] Unexpected error for job {job_id}:", e)
            return {}

        if state != current_state:
            print(f"[jobStatus] job {job_id} state={state}")
            current_state = state

        if message:
            print(f"[jobStatus] job {job_id} message={message}")

        if state in (lib.JobState.FAILED.value, lib.JobState.FINISHED.value):
            break

        sleep(poll_interval)

    try:
        if current_state == lib.JobState.FAILED.value:
            print(f"[jobOutcome] job {job_id} FAILED; fetching outcome for error details...")

        outcome = lib.job_outcome(client, ds, job_id)
        print(f"[jobOutcome] job {job_id} outcome:")
        print(outcome)
        return outcome

    except TransportQueryError as e:
        errors = getattr(e, "errors", []) or []
        if errors:
            for err in errors:
                msg = err.get("message")
                path = err.get("path")
                print(
                    f"[jobOutcome] GraphQL error for job {job_id}: "
                    f"{msg} (path={path})"
                )
        else:
            print(f"[jobOutcome] TransportQueryError for job {job_id}: {e}")
        return {}

    except Exception as e:
        print(f"[jobOutcome] Unexpected error for job {job_id}:", e)
        return {}


def start_optimization(poll_interval: float = 2.0) -> Tuple[int, dict]:

    field = ds.Mutation.startOptimization

    try:
        result = client.execute(dsl.dsl_gql(dsl.DSLMutation(field)))
    except TransportQueryError as e:
        print("[startOptimization] TransportQueryError:", e.errors or e)
        raise
    except Exception as e:
        print("[startOptimization] Unexpected error:", e)
        raise

    job_id = result["startOptimization"]
    print(f"[startOptimization] job_id={job_id}")

    outcome = poll_job_until_finished(job_id, poll_interval=poll_interval)
    return job_id, outcome





