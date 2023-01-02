# FastAPI set up

## Set up pyenv

### Create virtualenv

-   check for virtualenv: `pip list`
-   if you don't have virtualenv: `pip install virtualenv`
-   create venv: `python -m venv fastapienv`
-   activate the venv: `. fastapienv/bin/activate`. To deactivate:
    -   change directory to bin:
        `cd fastapienv/bin/`
    -   then: `$source deactivate`

### Install Dependencies

-   install FastAPI and dependencies: `pip install fastapi[all]`
    (seems to work on bash but not zsh)
