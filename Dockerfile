FROM python:3.8-slim

ENV TZ Europe/Moscow

WORKDIR /${PROJECT_NAME}
RUN pip install poetry

COPY pyproject.toml poetry.loc[k] ./
RUN poetry install --no-dev
COPY src ./src
COPY credentials.json .

COPY docker-entrypoint.sh .
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD [ "python", "-m", "src" ]
