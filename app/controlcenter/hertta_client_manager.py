from typing import Optional, Tuple
from time import sleep
from gql import dsl
from gql.dsl import DSLField
from . import hertta_client_lib as lib
from gql.transport.exceptions import TransportQueryError
import pathlib
from importlib import resources
import json

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

@lib.mutation
def load_model_json(model_json: str) -> dsl.DSLField:
    """Internal helper used by load_model_from_file; selects the MaybeError.message."""
    return lib.select_maybe_error(
        ds, ds.Mutation.loadModelJson.args(modelJson=model_json)
    )

def load_model_from_file(file_path: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    if file_path is None:
        try:
            model_json = resources.read_text(__package__, "elexia_model.json")
        except (FileNotFoundError, ModuleNotFoundError) as e:
            return False, f"resource not found: {e}"
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            model_json = f.read()

    mutation_field = ds.Mutation.loadModelJson.args(modelJson=model_json).select(
        ds.MaybeError.message
    )

    try:
        result = client.execute(dsl.dsl_gql(dsl.DSLMutation(mutation_field)))
    except Exception as e:
        return False, str(e)

    payload = result.get("loadModelJson", {})

    if payload.get("message") is None:
        return True, None

    return False, payload.get("message")

def update_time_line(
    step_hours: int, duration_hours: int
) -> Tuple[bool, Optional[list]]:
    """
    Update the model’s timeline; omit fields with zero values.
    Returns (True, None) on success or (False, validation_errors) on failure.
    """
    time_line_input = {}
    # Only include step if any component is > 0
    if step_hours > 0:
        time_line_input["step"] = {"hours": step_hours, "minutes": 0, "seconds": 0}
    # Only include duration if any component is > 0
    if duration_hours > 0:
        time_line_input["duration"] = {"hours": duration_hours, "minutes": 0, "seconds": 0}
    # If nothing to update, return success immediately
    if not time_line_input:
        return True, None

    errors_fragment = dsl.DSLFragment("TimeLineValidationErrors")
    errors_fragment.on(ds.ValidationErrors)
    errors_fragment.select(
        ds.ValidationErrors.errors.select(ds.ValidationError.field, ds.ValidationError.message)
    )
    field = ds.Mutation.updateTimeLine.args(timeLineInput=time_line_input).select(errors_fragment)
    result = client.execute(dsl.dsl_gql(dsl.DSLMutation(field), errors_fragment))
    payload = result["updateTimeLine"]
    return (True, None) if not payload.get("errors") else (False, payload["errors"])

def save_model() -> Tuple[bool, Optional[str]]:
    """
    Persist the current model to disk using the saveModel mutation.
    Returns (True, None) on success or (False, error message) on failure.
    """
    mutation_field = ds.Mutation.saveModel.select(ds.MaybeError.message)

    try:
        result = client.execute(dsl.dsl_gql(dsl.DSLMutation(mutation_field)))
    except Exception as e:
        return False, str(e)

    payload = result.get("saveModel", {})
    if payload.get("message") is None:
        return True, None
    return False, payload.get("message")

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





