# FastAPI Project - Backend

## Requirements

* [Docker](https://www.docker.com/).
* [uv](https://docs.astral.sh/uv/) for Python package and environment management.

## Docker Compose

Start the local development environment with Docker Compose following the guide in [../development.md](../development.md).

## General Workflow

By default, the dependencies are managed with [uv](https://docs.astral.sh/uv/), go there and install it.

From `./backend/` you can install all the dependencies with:

```console
$ uv sync
```

Then you can activate the virtual environment with:

```console
$ source .venv/bin/activate
```

Make sure your editor is using the correct Python virtual environment, with the interpreter at `backend/.venv/bin/python`.

Modify or add SQLModel models for data and SQL tables in `./backend/app/models.py`, API endpoints in `./backend/app/api/`, CRUD (Create, Read, Update, Delete) utils in `./backend/app/crud.py`.

## VS Code

There are already configurations in place to run the backend through the VS Code debugger, so that you can use breakpoints, pause and explore variables, etc.

The setup is also already configured so you can run the tests through the VS Code Python tests tab.

## Docker Compose Override

During development, you can change Docker Compose settings that will only affect the local development environment in the file `compose.override.yml`.

The changes to that file only affect the local development environment, not the production environment. So, you can add "temporary" changes that help the development workflow.

For example, the directory with the backend code is synchronized in the Docker container, copying the code you change live to the directory inside the container. That allows you to test your changes right away, without having to build the Docker image again. It should only be done during development, for production, you should build the Docker image with a recent version of the backend code. But during development, it allows you to iterate very fast.

There is also a command override that runs `fastapi run --reload` instead of the default `fastapi run`. It starts a single server process (instead of multiple, as would be for production) and reloads the process whenever the code changes. Have in mind that if you have a syntax error and save the Python file, it will break and exit, and the container will stop. After that, you can restart the container by fixing the error and running again:

```console
$ docker compose watch
```

There is also a commented out `command` override, you can uncomment it and comment the default one. It makes the backend container run a process that does "nothing", but keeps the container alive. That allows you to get inside your running container and execute commands inside, for example a Python interpreter to test installed dependencies, or start the development server that reloads when it detects changes.

To get inside the container with a `bash` session you can start the stack with:

```console
$ docker compose watch
```

and then in another terminal, `exec` inside the running container:

```console
$ docker compose exec backend bash
```

You should see an output like:

```console
root@7f2607af31c3:/app#
```

that means that you are in a `bash` session inside your container, as a `root` user, under the `/app` directory, this directory has another directory called "app" inside, that's where your code lives inside the container: `/app/app`.

There you can use the `fastapi run --reload` command to run the debug live reloading server.

```console
$ fastapi run --reload app/main.py
```

...it will look like:

```console
root@7f2607af31c3:/app# fastapi run --reload app/main.py
```

and then hit enter. That runs the live reloading server that auto reloads when it detects code changes.

Nevertheless, if it doesn't detect a change but a syntax error, it will just stop with an error. But as the container is still alive and you are in a Bash session, you can quickly restart it after fixing the error, running the same command ("up arrow" and "Enter").

...this previous detail is what makes it useful to have the container alive doing nothing and then, in a Bash session, make it run the live reload server.

## Backend tests

To test the backend run:

```console
$ bash ./scripts/test.sh
```

The tests run with Pytest, modify and add tests to `./backend/tests/`.

If you use GitHub Actions the tests will run automatically.

### Test running stack

If your stack is already up and you just want to run the tests, you can use:

```bash
docker compose exec backend bash scripts/tests-start.sh
```

That `/app/scripts/tests-start.sh` script just calls `pytest` after making sure that the rest of the stack is running. If you need to pass extra arguments to `pytest`, you can pass them to that command and they will be forwarded.

For example, to stop on first error:

```bash
docker compose exec backend bash scripts/tests-start.sh -x
```

### Test Coverage

When the tests are run, a file `htmlcov/index.html` is generated, you can open it in your browser to see the coverage of the tests.


## Email Templates

Once you have the MJML extension installed, you can create a new email template in the `src` directory. After creating the new email template and with the `.mjml` file open in your editor, open the command palette with `Ctrl+Shift+P` and search for `MJML: Export to HTML`. This will convert the `.mjml` file to a `.html` file and now you can save it in the build directory.

## Mock Alerting And Forecasting Data

For local demo runs, the repository includes a seed migration at `backend/sql_migrations/V24__seed_mock_alerting_forecasting_data.sql`.

That migration inserts a complete mock hospital setup with:

- one hospital
- doctors and attendance
- patients and disease history
- beds and occupancy pressure
- inventory with low stock and expiring items
- laboratories, kits, and equipment
- historical `daily_inventory_usage` and `daily_bed_stats`
- starter `forecasts` rows for bed occupancy, medicine demand, and kit demand

This data is intended to trigger the alerting rules and to give the forecasting functions enough history to produce results.

### How To Use It

Run your migrations as usual, then start the backend and work with the seeded records through the existing CRUD endpoints.

The alerting and forecasting logic does not currently have dedicated HTTP endpoints in this branch. Instead, it reads the database state that you create through the normal resource endpoints or through the seed migration.

### Request Values That Trigger Alerts

Use these payload shapes if you want to manually create data that will feed the alert engine:

Create a hospital:

```json
{
  "name": "Mock District Hospital",
  "district": "Mock District",
  "type": "District",
  "latitude": 18.5204,
  "longitude": 73.8567,
  "total_beds": 100,
  "created_at": "2026-07-08T00:00:00Z"
}
```

Create a doctor:

```json
{
  "hospital_id": 1001,
  "name": "Dr. Mock Sharma",
  "specialization": "General Medicine",
  "shift": "Day",
  "leave_status": "Available",
  "consultation_count": 42
}
```

Create a patient:

```json
{
  "hospital_id": 1001,
  "doctor_id": 5001,
  "disease_id": 2001,
  "age": 34,
  "gender": "M",
  "severity": "Moderate",
  "bed_required": false,
  "bed_allocated": false,
  "admission_status": "active",
  "registered_at": "2026-07-08T00:00:00Z"
}
```

Create inventory that can trigger low-stock and forecasted-shortage alerts:

```json
{
  "hospital_id": 1001,
  "medicine_id": 4001,
  "quantity": 8,
  "expiry_date": "2026-07-18",
  "reorder_level": 20,
  "updated_at": "2026-07-08T00:00:00Z"
}
```

Create a lab kit:

```json
{
  "laboratory_id": 6001,
  "test_name": "Dengue Rapid Test",
  "stock": 3,
  "threshold": 12
}
```

Create lab equipment:

```json
{
  "laboratory_id": 6001,
  "equipment_name": "CBC Analyzer",
  "status": "Needs Service",
  "last_service": "2025-11-30",
  "expected_life": 7,
  "usage_frequency": 40,
  "machine_age": 6
}
```

### Forecasting Inputs

The forecasting functions read historical tables, so the most useful rows are:

- `daily_inventory_usage` for medicine demand forecasts
- `daily_bed_stats` for bed occupancy forecasts
- `patient_tests` or `patients` history for disease and kit demand forecasts

The seed migration already provides realistic values, but if you want to add your own, keep these patterns in mind:

- low `quantity` compared to `reorder_level` triggers a low inventory alert
- `quantity` lower than a forecasted demand value triggers a forecasted shortage alert
- bed occupancy above `90%` triggers a current occupancy alert
- forecasted occupancy above `85%` triggers a warning alert
- a doctor marked `status = false` in `doctor_attendance` triggers a staffing alert
- a laboratory with `status != 'Operational'` triggers a lab availability alert
- equipment with `last_service` older than about 6 months triggers a maintenance alert
- repeated recent patient cases for the same disease can trigger a disease spike alert

### Example IDs Used By The Seed Data

- Hospital ID: `1001`
- Disease ID: `2001`
- Doctor ID: `5001`
- Laboratory ID: `6001`
- Medicine ID: `4001`
- Kit name: `Dengue Rapid Test`

Those values line up with the mock migration and are useful if you want to add more records manually.
