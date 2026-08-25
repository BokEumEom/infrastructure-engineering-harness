# public-api architecture

`public-api` is a high-criticality request-serving service.

## Responsibilities

- accept synchronous client requests
- validate identity and authorization through `identity-service`
- persist durable state through `primary-datastore`
- publish asynchronous work to `event-bus`

## Operational constraints

- datastore degradation can directly affect request latency and availability
- messaging degradation should not corrupt synchronous durable state
- telemetry backends are implementation choices; incident reasoning must rely on normalized evidence rather than a specific vendor
- production changes require a reversible rollout and explicit approval

## Failure domains to inspect

1. request-serving compute
2. datastore
3. identity dependency
4. messaging dependency
5. network path
6. recent deployment/configuration
