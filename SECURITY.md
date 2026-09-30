# Security policy

Security fixes are applied to the latest stable release.

Use GitHub private vulnerability reporting when available. Do not open a public issue containing credentials, tokens, private endpoints, customer data, or exploit details.

## Deployment guidance

- Use read-only Kubernetes RBAC unless an extension explicitly requires additional permissions.
- Store credentials in a secret manager or runtime secret store.
- Restrict outbound access to required telemetry and delivery endpoints.
- Run the container as a non-root user with a read-only filesystem and dropped capabilities.
- Validate pricing data and telemetry coverage before using recommendations for financial reporting.
