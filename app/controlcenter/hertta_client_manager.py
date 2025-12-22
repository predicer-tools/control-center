from typing import Optional
from gql import dsl
from gql.dsl import DSLField
from . import hertta_client_lib as lib

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
    """
    Call mutation:
        updateSettings(settingsInput: { location: { country, place } })

    Returns:
        (True, location_dict)    if settings were updated successfully
        (False, errors_list)    if ValidationErrors were returned
    """
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

def start_optimization():
    field = ds.Mutation.startOptimization
    result = client.execute(dsl.dsl_gql(dsl.DSLMutation(field)))
    job_id = result["startOptimization"]
    return client, ds, job_id


def run_building_optimization():

    ok, data = set_location("Finland", "Tampere")
    if not ok:
        print("[updateSettings ValidationErrors]", data)
    else:
        print("[updateSettings] New location:", data)


