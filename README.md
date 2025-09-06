# Avala Playground

This repo contains everything you need to try out Avala outside the competition environment. It includes the following:

- **Client workspace**: Example of what you should have in your local environment for developing and running exploits, with some fake exploits for trying out.
- **Mock game infra**: Mock service that generates random flag IDs and mock services that accept flags via HTTP and TCP.
- **Server workspace**: Example server configuration that works with the mock game infra.

## Getting started

Launch all containers in the following order:

1. Run mock infrastructure

    Review `compose.yaml` and adjust settings such as timezones or ports if needed. When done, run the containers using Docker Compose.

    ```console
    $ docker compose -f mock/compose.yaml up -d
    ```

2. Run server component

    Review all the files in `server` dictionary and modify according to the docs. Since multiple Docker networks are being created, it's recommended to use your machine's private IP address (run `hostname -I` and use the address beginning with `192`). Adjust settings in `compose.yaml` such as timezones, ports and similar.

    ```console
    $ docker compose -f server/compose.yaml up -d
    ```

3. Setup client environment

    Client environment is preconfigured to work with the configuration provided in `avala.yaml` file. To start playing with the Avala client, install `avala-ad` in a virtual environment and start running commands.

    ```console
    $ cd client
    $ python3 -m venv venv && source venv/bin/activate
    $ pip install avala-ad
    Successfully installed avala-ad-0.1.0
    ```
    ```console
    $ avl exploits
    wish
    wish_team_188 (draft)
    wish_experimental (draft)
    history_1
    history_2
    security.testing (draft)
    all_at_once
    ```
    ```console
    $ avl services
    history
    none
    own
    pay
    prepare
    security
    wish
    ```
    ```console
    $ avl flag-ids security 10.10.53.1
    ["nicole14@example.com", "simmonsholly@example.com", "fullermiranda@example.net", "stephanierobinson@example.com", "michael85@example.org"]
    (venv) $ avl launch wish_team_188
    [20:43:01] INFO     🚀 Launching exploit wish_team_188 (batch 1/1)...
    ...
    ```