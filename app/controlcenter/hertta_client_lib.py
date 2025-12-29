from collections.abc import Callable
from enum import auto, Enum, unique
from functools import wraps
import pathlib
import sys
import gql
from gql import Client, dsl
from gql.dsl import DSLField, DSLFragment, DSLSchema
from gql.transport.requests import RequestsHTTPTransport
from gql.utilities import update_schema_enum
from graphql import build_schema, DocumentNode


@unique
class ConstraintType(Enum):
    LESS_THAN = auto()
    EQUAL = auto()
    GREATER_THAN = auto()


@unique
class JobState(Enum):
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    FINISHED = "FINISHED"


@unique
class MarketType(Enum):
    ENERGY = auto()
    RESERVE = auto()


@unique
class Conversion(Enum):
    UNIT = auto()
    TRANSFER = auto()
    MARKET = auto()


def client_and_dsl(url) -> tuple[Client, DSLSchema]:
    with open(
        pathlib.Path(__file__).parent.parent / "schema", encoding="utf-8"
    ) as schema_file:
        schema = build_schema(schema_file.read())
    ds = dsl.DSLSchema(schema)
    transport = RequestsHTTPTransport(url=url)
    client = gql.Client(transport=transport, schema=schema)
    update_schema_enum(client.schema, "Conversion", Conversion)
    update_schema_enum(client.schema, "MarketType", MarketType)
    update_schema_enum(client.schema, "ConstraintType", ConstraintType)
    update_schema_enum(client.schema, "JobState", JobState)
    return client, ds


def execute_query(client: Client, operation: DocumentNode) -> dict:
    return client.execute(operation)


def execute_mutation(client: Client, operation: DocumentNode) -> None:
    result = client.execute(operation)
    for mutation_type, output in result.items():
        if "message" in output:
            if (error := output["message"]) is not None:
                raise RuntimeError(f"error in mutation: {error}")
        elif errors := output["errors"]:
            for error in errors:
                print(
                    f"{mutation_type}.{error['field']}: {error['message']}",
                    file=sys.stderr,
                )
            raise RuntimeError("validation errors in mutation")


def mutation(f: Callable[..., DSLField]) -> Callable[..., None]:
    @wraps(f)
    def wrapper(client: Client, *args, **kwargs):
        dsl_mutation = dsl.DSLMutation(f(*args, **kwargs))
        return execute_mutation(client, dsl.dsl_gql(dsl_mutation))

    return wrapper


def query(f: Callable[..., DSLField]) -> Callable[..., dict]:
    @wraps(f)
    def wrapper(client: Client, *args, **kwargs):
        dsl_query = dsl.DSLQuery(f(*args, **kwargs))
        return execute_query(client, dsl.dsl_gql(dsl_query))

    return wrapper


def select_validation_errors(ds: DSLSchema, field: DSLField) -> DSLField:
    return field.select(
        ds.ValidationErrors.errors.select(
            ds.ValidationError.field, ds.ValidationError.message
        ),
    )


def select_maybe_error(ds: DSLSchema, field: DSLField) -> DSLField:
    return field.select(ds.MaybeError.message)


def get_job_status(client: Client, ds: DSLSchema, job_id: int) -> tuple[JobState, str]:
    status = client.execute(
        dsl.dsl_gql(
            dsl.DSLQuery(
                ds.Query.jobStatus.args(jobId=job_id).select(
                    ds.JobStatus.state, ds.JobStatus.message
                )
            )
        )
    )
    status = status["jobStatus"]
    return status["state"], status["message"]


def job_outcome(client: Client, ds: DSLSchema, job_id: int):
    electricity_price_outcome = DSLFragment("ElectricityPriceOutcome")
    electricity_price_outcome.on(ds.ElectricityPriceOutcome)
    electricity_price_outcome.select(ds.ElectricityPriceOutcome.time, ds.ElectricityPriceOutcome.price)
    forecast_outcome = DSLFragment("ForecastOutcome")
    forecast_outcome.on(ds.WeatherForecastOutcome)
    forecast_outcome.select(
        ds.WeatherForecastOutcome.time, ds.WeatherForecastOutcome.temperature
    )
    optimization_outcome = DSLFragment("OptimizationOutcome")
    optimization_outcome.on(ds.OptimizationOutcome)
    optimization_outcome.select(
        ds.OptimizationOutcome.time,
        ds.OptimizationOutcome.controlSignals.select(
            ds.ControlSignal.name, ds.ControlSignal.signal
        ),
    )
    field = ds.Query.jobOutcome.args(jobId=job_id).select(
        electricity_price_outcome, forecast_outcome, optimization_outcome
    )
    result = client.execute(
        dsl.dsl_gql(dsl.DSLQuery(field), electricity_price_outcome, forecast_outcome, optimization_outcome)
    )
    command_output = result["jobOutcome"]
    return command_output
