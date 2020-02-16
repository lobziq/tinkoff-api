# tinkoff-api

> Python Tinkoff API client for asyncio and humans.

[![Latest Version](https://img.shields.io/pypi/v/tinkoff-api.svg)](https://pypi.python.org/pypi/tinkoff-api)
[![Python Version](https://img.shields.io/pypi/pyversions/tinkoff-api.svg)](https://pypi.python.org/pypi/tinkoff-api)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


In active development.

Table of contens
--------------------------------------------------------------------------------
* [Installation](#installation)
* [Usage examples](#usage-examples)
    * [REST API client](#rest-api-client)
    * [Streaming client](#streaming-client)
    * [Dynamic subscriptions in runtime](#dynamic-subscriptions-in-runtime)
* [TODO](#todo)


Installation
--------------------------------------------------------------------------------

Use pip to install:
```shell
$ pip install tinkoff-api
```

Usage examples
--------------------------------------------------------------------------------

#### REST API client:
```python
import asyncio
from datetime import datetime

from tinkoff.investments.client import TinkoffInvestmentsRESTClient
from tinkoff.investments.client.environments import Environment
from tinkoff.investments.model.market.candles import CandleResolution
from tinkoff.investments.client.exceptions import TinkoffInvestmentsError

async def show_apple_year_candles():
    try:
        async with TinkoffInvestmentsRESTClient(
                token='TOKEN',
                environment=Environment.SANDBOX) as client:

            candles = await client.market.candles.get(
                figi='BBG000B9XRY4',
                dt_from=datetime(2019, 1, 1),
                dt_to=datetime(2019, 12, 31),
                interval=CandleResolution.DAY
            )
            for candle in candles:
                print(f'{candle.time}: {candle.h}')
    except TinkoffInvestmentsError as e:
        print(e)


async def jackpot():
    try:
        async with TinkoffInvestmentsRESTClient(
                token='TOKEN',
                environment=Environment.SANDBOX) as client:

            instruments = await client.market.instruments.search(ticker='AAPL')
            apple = instruments[0]

            account = await client.sandbox.accounts.register()
            await client.sandbox.accounts.positions.set_balance(
                broker_account_id=account.brokerAccountId,
                figi=apple.figi,
                balance=100,
            )

            print('We created the following portfolio:')
            positions = await client.portfolio.get_positions()
            for position in positions:
                print(f'{position.name}: {position.lots} lots')
    except TinkoffInvestmentsError as e:
        print(e)

asyncio.run(jackpot())
```

#### Streaming Client:
```python
import asyncio

from tinkoff.investments.client.streaming import StreamingClient, EventsBroker
from tinkoff.investments.model.streaming import CandleEvent, CandleResolution

events = EventsBroker()

@events.candles('BBG009S39JX6', CandleResolution.MIN_1)
@events.candles('BBG000B9XRY4', CandleResolution.MIN_1)
async def on_candle(candle: CandleEvent):
    print(candle)

async def main():
    client = StreamingClient(token='TOKEN', events=events)
    await client.run()

asyncio.run(main())
```

#### Dynamic subscriptions in runtime:
```python
import asyncio

from tinkoff.investments.client.streaming import StreamingClient, EventsBroker
from tinkoff.investments.model.streaming import CandleEvent, CandleResolution, \
    OrderBookEvent

events = EventsBroker()

@events.candles('BBG000B9XRY4', CandleResolution.HOUR)
async def on_candle(candle: CandleEvent):
    if candle.h > 1000:
        await events.candles.subscribe(
            callback=on_candle,
            figi=candle.figi,
            interval=CandleResolution.MIN_1
        )
    elif candle.h < 1000:
        await events.candles.unsubscribe(candle.figi, CandleResolution.MIN_1)


async def main():
    client = StreamingClient(token='TOKEN', events=events)
    await client.run()

asyncio.run(main())
```

TODO
--------------------------------------------------------------------------------

* allow to provide str constants along with specific enum objects
* add configurable timeouts in streaming client
* add ability to unsubscribe by pattern
* rename some fields
* make some fields in snake case
* generate documentation
