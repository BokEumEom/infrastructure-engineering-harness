# Decision Records

This directory is the canonical home for durable project architecture and policy decisions.

Use a decision record when future maintainers are likely to ask **why** a consequential choice was made. Keep current-state descriptions in the relevant architecture or contract document instead.

## What belongs here

A decision record should capture:

- the decision and status;
- the context and constraints that made the decision necessary;
- meaningful alternatives considered;
- consequences and trade-offs;
- links to the current canonical documents affected by the decision.

Use a stable numeric prefix when adding records, for example:

~~~text
0001-provider-neutral-runtime.md
0002-progressive-context-loading.md
~~~

Do not use this directory for runtime fixtures. Example ADR data under examples/ exists to exercise contracts and is not a project architecture decision log.

Return to the [documentation index](../README.md).
