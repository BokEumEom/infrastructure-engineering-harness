# orders-api architecture

## Runtime

`orders-api` runs on ECS Fargate behind an application load balancer.

## Data path

```text
Client
  ↓
Application Load Balancer
  ↓
ECS Fargate: orders-api
  ├─ Aurora: aurora-orders
  └─ Event stream: event-stream
```

## Operational characteristics

- Stateless application tasks may scale horizontally.
- `aurora-orders` is a stateful, high-criticality dependency.
- Database saturation can increase API latency even when ECS CPU remains healthy.
- Production changes should be made through reviewed infrastructure code.

## Observability

- Application traces and logs: Datadog
- Infrastructure metrics: CloudWatch
- Primary service objectives are defined in `service-catalog.yaml`.
