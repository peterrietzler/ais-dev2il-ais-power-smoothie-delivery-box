FROM debian:bookworm-slim

# Set the working directory
WORKDIR /app

# Install curl and ca-certificates to be able to download uv
RUN apt-get update && apt-get install -y curl ca-certificates && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy the application code
COPY . .

# Install dependencies
RUN uv sync --frozen

# Set the entrypoint
CMD ["uv", "run", "main.py"]
