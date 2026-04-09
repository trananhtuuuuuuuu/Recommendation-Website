# Agents

This document describes the responsibilities and purpose of each logical layer ("agent") in the project.

- **API**: Defines HTTP endpoints and request/response contracts. Location: app/api and app/api/v1. Responsibilities: routing, request validation, authentication, and mapping HTTP requests to service calls.
- **Core**: Shared application-level concerns such as exception classes, security helpers, providers, and unit-of-work abstractions. Location: app/core. Responsibilities: define exceptions, configuration, and cross-cutting utilities.
- **DB**: Database connection and session management. Location: app/db. Responsibilities: engine/session setup, connection utilities, and migrations entrypoints.
- **Mapper**: Transform request DTOs to domain entities and entities to response DTOs. Location: app/mappers. Responsibilities: pure data transformations and lightweight validation.
- **Repositories**: Data access abstractions (ORM queries and persistence). Location: app/repositories. Responsibilities: CRUD operations, query composition, and transaction boundaries when required by the UoW.
- **Services**: Business logic that orchestrates repositories, mappers, and core components. Location: app/services. Responsibilities: use-case implementations, domain rules, and transaction management.

**Guidelines**

- Keep transport concerns in the API layer, persistence in repositories, and business rules in services.
- Mappers should be side-effect-free and only perform transformations/formatting.
- Repositories must not perform HTTP handling or input validation.
- Use dependency injection via `core/provider.py` and transaction management via `core/uow.py` where appropriate.
- write unit test for each time after implementating any features and automatically fix if errors occur

**How to add a new agent/component**

1. Create the module under the appropriate folder (api, core, db, mappers, repositories, or services).
2. Add focused unit tests covering behavior.
3. Register the component with the provider or add the API route and wiring.
4. Keep changes small and follow existing conventions (see CONVENTIONS.md).
