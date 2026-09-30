FROM python:3.12-slim
WORKDIR /app
RUN useradd --create-home --uid 65532 appuser
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir '.[api]'
USER 65532:65532
EXPOSE 8080
CMD ["uvicorn", "finops_agent.api:app", "--host", "0.0.0.0", "--port", "8080"]
