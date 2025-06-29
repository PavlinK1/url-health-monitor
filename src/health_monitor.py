#!/usr/bin/env python3
"""
health_monitor.py

A simple Prometheus exporter that checks the availability and
response timeof two external URLs and exposes their metrics.
"""

import time
import requests
from prometheus_client import (
    start_http_server,
    Gauge,
    REGISTRY,
    PROCESS_COLLECTOR,
    PLATFORM_COLLECTOR,
    GC_COLLECTOR,
)

# Remove the default Prometheus collectors so only our custom metrics are exposed
for collector in (PROCESS_COLLECTOR, PLATFORM_COLLECTOR, GC_COLLECTOR):
    try:
        REGISTRY.unregister(collector)
    except KeyError:
        # Collector was already removed
        pass

# Define our custom metrics
url_up = Gauge(
    'sample_external_url_up',
    'External URL availability (1 = up, 0 = down)',
    ['url']
)
url_response_ms = Gauge(
    'sample_external_url_response_ms',
    'External URL response time in milliseconds',
    ['url']
)

# List of URLs to monitor
URLS = [
    'https://httpstat.us/503',
    'https://httpstat.us/200'
]

def check_urls():
    """Check each URL and update the Prometheus metrics."""
    for url in URLS:
        start_time = time.time()
        try:
            response = requests.get(url, timeout=5)
            latency = (time.time() - start_time) * 1000  # convert to ms
            status = 1 if response.status_code == 200 else 0
        except requests.RequestException:
            # On any request error, mark the URL as down
            latency = (time.time() - start_time) * 1000
            status = 0

        # Update Prometheus gauges
        url_up.labels(url=url).set(status)
        url_response_ms.labels(url=url).set(latency)

if __name__ == '__main__':
    # Start an HTTP server on port 8000 to expose metrics
    start_http_server(8000)
    print("Prometheus metrics available at http://localhost:8000")

    # Run the check every 10 seconds
    while True:
        check_urls()
        time.sleep(10)
