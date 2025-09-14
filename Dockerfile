FROM python:3.12-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock ./

# Sync dependencies
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY . .

# Expose any ports if needed (adjust as necessary)
# EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["uv", "run", "python", "src/mcp_pipe.py", "src/coze_req.py"]