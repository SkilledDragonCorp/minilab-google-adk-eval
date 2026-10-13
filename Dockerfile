FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev
ENV PYTHONPATH=/app/src
EXPOSE 8000
CMD ["uv", "run", "adk", "api_server", "src/adk_lab", "--host", "0.0.0.0", "--port", "8000"]
