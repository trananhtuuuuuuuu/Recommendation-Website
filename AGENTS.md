# Agents
# The description for why this project is created
- Let's read "deep_learning_phan_tich_CV.pdf" file name to understanding
# This document describes the responsibilities and purpose of each logical layer ("agent") in the project.
# Folder architecture
- **app/API**: Defines HTTP endpoints and request/response contracts. Location: app/api: init or declare and a api for testing something and app/api/v1: contain all of features related to entities also involve __init__.py file for definition. Responsibilities: routing, call logic service.
- **app/Core**: Shared application-level concerns such as exception classes, security helpers, providers, and unit-of-work abstractions. Location: app/core. Responsibilities: define exceptions, configuration, security configuration, uow.
- **app/DB**: Database connection and session management. Location: app/db. Responsibilities: engine/session setup, connection utilities, and migrations entrypoints.
- **app/Mapper**: Transform request DTOs to domain entities and entities to response DTOs. Location: app/mappers. Responsibilities: pure data transformations and lightweight validation.
- **app/Repositories**: Data access abstractions (ORM queries and persistence). Location: app/repositories. Responsibilities: CRUD operations, query composition, and transaction boundaries when required by the UoW.
- **app/Services**: Business logic that orchestrates repositories, mappers, and core components. Location: app/services. Responsibilities: use-case implementations, domain rules, and transaction management, validate request, mapper request, call to repository.
- **app/models**: contain whole entities related directly to this project
- **app/utils**: place for utilities functions
- **app/tests**: place for implement tests
- **app/schemas**: place for request and response, Location: schemas/request/user: everything related to request from user, inside that exist the subfolder for applicant and recruiter 
- **app/migrations**: contain files related to changes about entities
- **deployment**: place for deployment process by using github like a remote control
- **docker**: place containing whole docker files such as: Dockerfile.client (Dockerfile for frontend side), Dockerfile.server (Dockerfile for backend side), docker-compose.yml (docker-compose file for whole project)
- **client** place contain whole src code related directly to frontend side by using react typescript, tailwind for css
- **piplines**: contain files for building pipline automatically

# Command files 
- **docker-command.md**: for each Dockerfile you write let's add instructions for reason why this file existed and how can i run this file and the detail explaination on its
- "run.py": file for running this project 

**Guidelines**
- currently in my design still have not existed dependency injection yet, i want to create InternalProvider to apply dependency injection in my design
- exception handling i want to use pydantic by using @field decorator to define a message for a field 
- for each api built i need you write intergration test for them
- let's suggest for me create a .env file and put all variables that related to this project inside that
- let's clearly and detailly instruct for me the authentication feature with username and password and return for client with access_token and refresh_token
- for each features you write or implement, let's use dependency injection and clean code for me via InternalProvider
- currently my architecture design still unclear you can create new file or remove already existed files if necessary

# Features
- /api/v1/jobs: view all jobs with active status


