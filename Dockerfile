# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ADD ./ fetch-code-challenge-2025/
WORKDIR fetch-code-challenge-2025

ENV PYTHONPATH /fetch-code-challenge-2025
# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
RUN uv sync --project . --no-dev -v

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []
CMD ["uv", "run", "flask", "run", "--debug", "--host=0.0.0.0"]