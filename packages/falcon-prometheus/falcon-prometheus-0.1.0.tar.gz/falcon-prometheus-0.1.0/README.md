# falcon-prometheus

A falcon middleware to export Prometheus metrics.

## Installation
`pip install falcon-prometheus`

## Usage

Using prometheus-metrics is as simple as setting middleware, and adding a route.

```bash
import falcon
from falcon_prometheus import PrometheusMiddleware

exporter = PrometheusMetrics()

api = falcon.API(middleware=exporter)
api.add_route('/metrics', exporter)
```

## Supported Labels
Currently supported labels are:
* `req.method`
* `req.path`
* `resp.status`

## Todo
* Add a counter for errors
* Tests