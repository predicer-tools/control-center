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
def set_setup() -> DSLField:
    setup = {
        "containsReserves": False,
        "containsOnline": False,
        "containsStates": True,
        "containsPiecewiseEff": False,
        "containsRisk": False,
        "containsDiffusion": True,
        "containsDelay": False,
        "containsMarkets": True,
        "reserveRealisation": True,
        "useMarketBids": True,
        "commonTimesteps": 0,
        "commonScenarioName": '"ALL"',
        "useNodeDummyVariables": True,
        "useRampDummyVariables": True,
        "nodeDummyVariableCost": 10000.0,
        "rampDummyVariableCost": 10000.0,
    }
    field = lib.select_validation_errors(
        ds, ds.Mutation.updateInputDataSetup.args(setupUpdate=setup)
    )
    return field


@lib.mutation
def add_scenario(name: str, weight: float) -> DSLField:
    return lib.select_maybe_error(
        ds, ds.Mutation.createScenario(name=name, weight=weight)
    )


@lib.mutation
def add_process_group(name: str) -> DSLField:
    return lib.select_maybe_error(ds, ds.Mutation.createProcessGroup(name=name))


@lib.mutation
def add_node_group(name: str) -> DSLField:
    return lib.select_validation_errors(ds, ds.Mutation.createNodeGroup(name=name))


@lib.mutation
def add_node(name: str, is_market: bool = False) -> DSLField:
    field = lib.select_validation_errors(
        ds,
        ds.Mutation.createNode.args(
            node={
                "name": name,
                "isCommodity": False,
                "isMarket": is_market,
                "isRes": False,
                "cost": None,
                "inflow": None,
            }
        ),
    )
    return field


@lib.mutation
def set_node_state(name: str, state: dict) -> DSLField:
    return lib.select_validation_errors(
        ds, ds.Mutation.setNodeState.args(state=state, nodeName=name)
    )


@lib.mutation
def connect_node_inflow_to_temperature_forecast(node_name: str) -> DSLField:
    return lib.select_maybe_error(
        ds,
        ds.Mutation.connectNodeInflowToTemperatureForecast.args(
            nodeName=node_name, forecastName="whatever"
        ),
    )


@lib.query
def node_names() -> DSLField:
    field = ds.Query.model.select(
        ds.Model.input_data.select(
            ds.InputData.nodes.select(
                ds.Node.name, ds.Node.state.select(ds.State.inMax, ds.State.outMax)
            )
        )
    )
    return field


@lib.mutation
def add_process(name: str, conversion: lib.Conversion) -> DSLField:
    field = lib.select_validation_errors(
        ds,
        ds.Mutation.createProcess.args(
            process={
                "name": name,
                "conversion": conversion,
                "isCfFix": False,
                "isOnline": False,
                "isRes": False,
                "eff": 1.0,
                "loadMin": 0.0,
                "loadMax": 1.0,
                "startCost": 0.0,
                "minOnline": 0,
                "minOffline": 0,
                "maxOnline": 0,
                "maxOffline": 0,
                "initialState": True,
                "isScenarioIndependent": False,
            }
        ),
    )
    return field


@lib.mutation
def add_process_to_group(process: str, group: str) -> DSLField:
    return lib.select_maybe_error(
        ds, ds.Mutation.addProcessToGroup.args(processName=process, groupName=group)
    )


@lib.mutation
def add_topology(
    source: Optional[str], process: str, sink: Optional[str], topology: dict
) -> DSLField:
    return lib.select_validation_errors(
        ds,
        ds.Mutation.createTopology.args(
            topology=topology,
            processName=process,
            sourceNodeName=source,
            sinkNodeName=sink,
        ),
    )


@lib.mutation
def add_node_diffusion(source: str, sink: str, coefficient: float) -> DSLField:
    return lib.select_validation_errors(
        ds,
        ds.Mutation.createNodeDiffusion.args(
            fromNode=source, toNode=sink, coefficient=coefficient
        ),
    )


@lib.mutation
def add_market(name: str) -> DSLField:
    return lib.select_validation_errors(
        ds,
        ds.Mutation.createMarket.args(
            market={
                "name": name,
                "mType": lib.MarketType.ENERGY,
                "node": "electricitygrid",
                "processGroup": "p1",
                "direction": None,
                "realisation": None,
                "reserveType": None,
                "isBid": True,
                "isLimited": False,
                "minBid": 0.0,
                "maxBid": 0.0,
                "fee": 0.0,
                "price": None,
                "upPrice": None,
                "downPrice": None,
                "reserveActivationPrice": None,
            }
        ),
    )


@lib.mutation
def connect_market_prices_to_forecast(market_name: str) -> DSLField:
    return lib.select_maybe_error(
        ds,
        ds.Mutation.connectMarketPricesToForecast.args(
            marketName=market_name, forecastName="whatever"
        ),
    )


@lib.mutation
def add_risk(parameter: str, value: float) -> DSLField:
    return lib.select_validation_errors(
        ds,
        ds.Mutation.createRisk.args(
            risk={
                "parameter": parameter,
                "value": value,
            }
        ),
    )


@lib.mutation
def add_generic_constraint(name: str, operator: lib.ConstraintType) -> DSLField:
    return lib.select_validation_errors(
        ds,
        ds.Mutation.createGenConstraint.args(
            constraint={
                "name": name,
                "gcType": operator,
                "isSetpoint": True,
                "penalty": 15.0,
                "constant": None,
            }
        ),
    )


@lib.mutation
def add_state_constraint_factor(factor: float, constraint: str, node: str) -> DSLField:
    return lib.select_validation_errors(
        ds,
        ds.Mutation.createStateConFactor(
            factor=factor, constraintName=constraint, nodeName=node
        ),
    )


def start_optimization() -> int:
    field = ds.Mutation.startOptimization
    result = client.execute(dsl.dsl_gql(dsl.DSLMutation(field)))
    command_output = result["startOptimization"]
    return command_output


def run_building_optimization():
    clear_model(client)
    add_scenario(client, "S1", 1.0)
    set_setup(client)
    add_process_group(client, "p1")
    add_process(client, "electricheater", lib.Conversion.UNIT)
    add_process_to_group(client, "electricheater", "p1")
    add_process(client, "dhw_heater", lib.Conversion.UNIT)
    add_process_to_group(client, "dhw_heater", "p1")
    add_process(client, "electricitygrid_npe_trade_process", lib.Conversion.MARKET)
    add_node(client, "interiorair")
    set_node_state(
        client,
        "interiorair",
        {
            "inMax": 1000000000.0,
            "outMax": 1000000000.0,
            "stateLossProportional": 0.0,
            "stateMax": 308.15,
            "stateMin": 273.15,
            "initialState": 292.15,
            "isScenarioIndependent": False,
            "isTemp": True,
            "tEConversion": 0.5,
            "residualValue": 0.0,
        },
    )
    add_node(client, "buildingenvelope")
    set_node_state(
        client,
        "buildingenvelope",
        {
            "inMax": 1000000000.0,
            "outMax": 1000000000.0,
            "stateLossProportional": 0.0,
            "stateMax": 308.15,
            "stateMin": 238.15,
            "initialState": 282.0,
            "isScenarioIndependent": False,
            "isTemp": True,
            "tEConversion": 1.0,
            "residualValue": 0.0,
        },
    )
    add_node(client, "outside")
    set_node_state(
        client,
        "outside",
        {
            "inMax": 1000000000.0,
            "outMax": 1000000000.0,
            "stateLossProportional": 0.0,
            "stateMax": 308.15,
            "stateMin": 238.15,
            "initialState": 269.5,
            "isScenarioIndependent": False,
            "isTemp": True,
            "tEConversion": 1000000000.0,
            "residualValue": 0.0,
        },
    )
    connect_node_inflow_to_temperature_forecast(client, "outside")
    add_node(client, "electricitygrid")
    add_node(client, "dhw")
    set_node_state(
        client,
        "dhw",
        {
            "inMax": 1000000000.0,
            "outMax": 1000000000.0,
            "stateLossProportional": 0.0,
            "stateMax": 20.0,
            "stateMin": 0.0,
            "initialState": 10.0,
            "isScenarioIndependent": False,
            "isTemp": False,
            "tEConversion": 1.0,
            "residualValue": 0.0,
        },
    )
    add_node(client, "npe", is_market=True)
    add_topology(
        client,
        "electricitygrid",
        "electricheater",
        None,
        {
            "capacity": 7.0,
            "vomCost": 0.0,
            "rampUp": 1.0,
            "rampDown": 1.0,
            "initialLoad": 0.7,
            "initialFlow": 0.7,
            "capTs": None,
        },
    )
    add_topology(
        client,
        None,
        "electricheater",
        "interiorair",
        {
            "capacity": 7.0,
            "vomCost": 0.0,
            "rampUp": 1.0,
            "rampDown": 1.0,
            "initialLoad": 0.7,
            "initialFlow": 0.7,
            "capTs": None,
        },
    )
    add_topology(
        client,
        "electricitygrid",
        "dhw_heater",
        None,
        {
            "capacity": 3.0,
            "vomCost": 0.0,
            "rampUp": 1.0,
            "rampDown": 1.0,
            "initialLoad": 0.7,
            "initialFlow": 0.7,
            "capTs": None,
        },
    )
    add_topology(
        client,
        None,
        "dhw_heater",
        "dhw",
        {
            "capacity": 3.0,
            "vomCost": 0.0,
            "rampUp": 1.0,
            "rampDown": 1.0,
            "initialLoad": 0.7,
            "initialFlow": 0.7,
            "capTs": None,
        },
    )
    add_topology(
        client,
        "electricitygrid",
        "electricitygrid_npe_trade_process",
        "npe",
        {
            "capacity": 0.0,
            "vomCost": 1e-5,
            "rampUp": 1.0,
            "rampDown": 1.0,
            "initialLoad": 1.0,
            "initialFlow": 1.0,
            "capTs": None,
        },
    )
    add_topology(
        client,
        "npe",
        "electricitygrid_npe_trade_process",
        "electricitygrid",
        {
            "capacity": 0.0,
            "vomCost": 0.0,
            "rampUp": 1.0,
            "rampDown": 1.0,
            "initialLoad": 1.0,
            "initialFlow": 1.0,
            "capTs": None,
        },
    )
    add_node_diffusion(client, "interiorair", "buildingenvelope", 0.25)
    add_node_diffusion(client, "buildingenvelope", "outside", 0.2)
    add_market(client, "npe")
    connect_market_prices_to_forecast(client, "npe")
    add_risk(client, "alfa", 0.1)
    add_risk(client, "beta", 0.0)
    add_generic_constraint(client, "c_interiorair_up", lib.ConstraintType.LESS_THAN)
    add_state_constraint_factor(client, 298.15, "c_interiorair_up", "interiorair")
    add_generic_constraint(client, "c_interiorair_down", lib.ConstraintType.GREATER_THAN)
    add_state_constraint_factor(client, 292.15, "c_interiorair_down", "interiorair")

    job_id = start_optimization()
    return client, ds, job_id

    # while True:
    #     state, message = lib.get_job_status(client, ds, job_id)
    #     print(f"{state}: {message}")
    #     # log_signal.emit(f"{state}")
    #     if state == lib.JobState.FAILED.value or state == lib.JobState.FINISHED.value:
    #         # log_signal.emit(f"Job finished with state:{state}")
    #         break
    #     sleep(3.0)

    # print(lib.job_outcome(client, ds, job_id))
