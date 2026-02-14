# AIS DEV2IL 😈 Power Smoothies In a Box

## 🐳 Docker Container Playground

Welcome to the Docker Container Playground! Before we can deliver power smoothies in containers, we need to master the art 
of container management. This exercise will teach you the fundamental Docker commands you'll use every day as a developer.

### 🛠 Tools You'll Need
- Docker Desktop installed and running
- Your terminal

Check Docker is Running:
```bash
docker --version
```
You should see something like `Docker version 29.x.x`.

### The Basics: Running and Managing Containers

#### Your First Container

Let's start with the classic Docker introduction: `hello-world`.

```bash
docker run hello-world
```

**What has just happened?**
1. Docker looked for the `hello-world` image locally
2. Didn't find it, so it pulled it from Docker Hub
3. Created a container from that image
4. Ran the container (which prints a message)
5. The container exited

Let's see what containers we have:

```bash
docker ps
```

🤔 Nothing? That's because `docker ps` only shows **running** containers. Our `hello-world` container already finished and exited.

See all containers (including stopped ones):

```bash
docker ps -a
```

✅ There it is! You'll see your hello-world container with a status of `Exited`.

💡 **Learning Point:** Containers are ephemeral. They run, do their job, and stop. Unlike virtual machines, 
they don't keep running unless they have a reason to.

### Fun with Cowsay 🐮

Let's have some fun! There's a container that makes a cow say things.

```bash
docker run rancher/cowsay "Hello Docker"
```

🐄 A cow should appear in your terminal with your message!

Try different messages:

```bash
docker run rancher/cowsay "I love containers"
docker run rancher/cowsay "DevOps is awesome"
```

Check your containers again:

```bash
docker ps -a
```

😱 Wow! Look at all those stopped containers. Each `docker run` created a new container. They're piling up!

Let's clean up one of them:

Find a container ID from the list above (you only need the first few characters), then remove it:

```bash
docker rm <container-id>
```

For example, if the ID is `a1b2c3d4e5f6`, you can just type:

```bash
docker rm a1b2
```

Run `docker ps -a` again. That container is gone!

💡 Deleting containers one by one gets tedious. There's a better way...

The `--rm` flag to the rescue:

```bash
docker run --rm rancher/cowsay "Chuck Norris can delete containers before they start"
```

Check `docker ps -a` again. This container automatically removed itself after running! The `--rm` flag tells Docker to delete 
the container as soon as it stops.

💡 **Best Practice:** Use `--rm` for one-off commands to keep your system clean.

### Step 3: Interactive Containers

So far, containers have just run a command and exited. Let's actually go **inside** a container! We are going to 
use `busybox` for this purpose. 

**What is busybox?**

BusyBox is a tiny Linux system that contains many common Unix tools (like `ls`, `cat`, `echo`, `grep`) bundled into a single small executable. 
It's perfect for learning Docker because:
- 🪶 Super lightweight (only ~1-5 MB)
- ⚡ Downloads quickly
- 🔧 Has all the basic tools you need to explore
- 🎯 Simple and doesn't distract from learning Docker concepts

Run busybox interactively:

```bash
docker run -it --rm busybox sh
```

🎯 You're now **inside** the container! Your terminal prompt changed. You have a shell (`sh`) running inside an isolated Linux environment.

Try some commands:

```sh
ls
pwd
echo "Hello from inside a container!"
hostname
```

Exit the container:

```sh
exit
```

You're back on your host machine. The busybox container is stopped.

💡 What do the `-it` flags mean?
- `-i` = Interactive (keep STDIN open)
- `-t` = Allocate a pseudo-TTY (a terminal)
- Together they let you interact with the container like a normal shell.

#### Long-Running Containers

Real-world containers usually run services that keep going. 
Let's simulate that with a container that outputs the current time every second.

Run a "ticker" container in the background:

```bash
docker run -d --name my-ticker busybox sh -c "while true; do date; sleep 1; done"
```

🆕 New flags:
- `-d` = Detached mode (runs the container in the background)
- `--name my-ticker` = Gives the container a friendly name instead of a random one

Check that it's running:

```bash
docker ps
```

✅ You should see `my-ticker` in the list with a status of `Up`.

Want to know what's it doing? Check the logs:

```bash
docker logs my-ticker
```

You'll see a bunch of timestamps! Each one is from a `date` command the container executed.

Watch the logs in real-time:

```bash
docker logs -f my-ticker
```

💡 The `-f` flag means "follow" - you'll see new timestamps appear every second. 
This is like `tail -f` for container logs.

Press `Ctrl+C` to stop following the logs (the container keeps running).

#### Container Lifecycle Management

Now let's practice stopping, starting, and restarting containers.

Stop the ticker:

```bash
docker stop my-ticker
```

Check its status:

```bash
docker ps
```

It's gone from the running list!

```bash
docker ps -a
```

There it is, with status `Exited`.

Start it again:

```bash
docker start my-ticker
```

Check the logs:

```bash
docker logs my-ticker
```

🎯 Notice the gap in timestamps? The container stopped, and when you started it, 
the loop continued with fresh timestamps.

Restart the container:

```bash
docker restart my-ticker
```

This is equivalent to `stop` + `start` in one command.

💡 **The Lifecycle:**
- `run` = Create a **new** container and start it
- `stop` = Stop a running container
- `start` = Start a stopped container
- `restart` = Restart a running or stopped container

#### Executing Commands in Running Containers

What if you want to open a shell inside a container that's already running? 
That's what `docker exec` is for!

Make sure your ticker is running:

```bash
docker ps
```

Execute a shell inside the running container:

```bash
docker exec -it my-ticker sh
```

🎯 You're now **inside** the container! But unlike `docker run`, you didn't create 
a new container - you connected to the existing one.

Explore while inside:

```sh
ps
```

You should notice that the `date` loop is running as a process in the container. 
You can also run other commands or even start a new process.

Exit when done:

```sh
exit
```

The container keeps running! Check with `docker ps`.

💡 **`run` vs `exec`:**
- `docker run` = Create and start a **new** container
- `docker exec` = Execute a command in an **existing** running container

You can use `exec` to troubleshoot or interact with a container without stopping it. And you 
also don't have to use a terminal, like we did here. Let's run the same command as above without
a terminal:

```sh
docker exec my-ticker ps 
```

#### Container Housekeeping

Time to clean up! Containers and images take up disk space, so it's important to remove 
what you don't need.

List all containers:

```bash
docker ps -a
```

Stop any running containers:

```bash
docker stop my-ticker
```

**Remove containers by name:**

```bash
docker rm my-ticker
```

Remove the hello-world containers too:

You can remove by name or by container ID (from `docker ps -a`). Let's do it by ID:

```bash
docker ps -a
docker rm <container-id> <container-id> <container-id>
```

You can also use  
```bash
docker container prune
```
to remove all stopped containers at once. 
Be **very** careful with this command. There's no way to undo it and if a container
has e.g. created or changed any files within the container, those will be lost forever.


List images:

```bash
docker images
```

You'll see `hello-world`, `rancher/cowsay`, and `busybox`.

Remove images:

```bash
docker rmi hello-world
docker rmi rancher/cowsay
docker rmi busybox
```

Or remove all unused images:

```bash
docker image prune -a
```

Unlike containers, images are usually safer to delete as you can always pull them again 
from Docker Hub.

### 🚀 Level Up

Finished early? Put your Docker skills to the test with these advanced moves.

#### Challenge 1: Container Naming and Filtering

Names make containers easier to manage. Let's practice!

**Start multiple ticker containers with descriptive names:**

```bash
docker run -d --name ticker-1 busybox sh -c "while true; do echo 'Ticker 1:' $(date); sleep 1; done"
docker run -d --name ticker-2 busybox sh -c "while true; do echo 'Ticker 2:' $(date); sleep 1; done"
docker run -d --name ticker-3 busybox sh -c "while true; do echo 'Ticker 3:' $(date); sleep 1; done"
```

List all containers:

```bash
docker ps
```

Use filters to find specific containers:

```bash
docker ps --filter "name=ticker"
```

This shows only containers with "ticker" in the name!

Try other filters:

```bash
docker ps --filter "status=running"
docker ps --filter "status=exited"
```

Clean up:

```bash
docker stop ticker-1 ticker-2 ticker-3
docker rm ticker-1 ticker-2 ticker-3
```

#### Challenge 2: Inspect Container Details

Docker stores a lot of metadata about containers. Let's dig in!

Start a container:

```bash
docker run -d --name inspector busybox sh -c "while true; do date; sleep 1; done"
```

Inspect the container:

```bash
docker inspect inspector
```

😱 That's a lot of JSON! Let's extract specific information.

Find the the time the container was started:

```bash
docker inspect inspector | grep StartedAt
```

Or use Docker's built-in formatting:

```bash
docker inspect --format='{{.State.StartedAt}}' inspector
```

Find the command it's running:

```bash
docker inspect --format='{{.Config.Cmd}}' inspector
```

💡 `docker inspect` is incredibly useful for debugging container issues!

Clean up:

```bash
docker stop inspector
docker rm inspector
```

#### Challenge 3: Monitor Resource Usage

Want to see how much CPU and memory your containers are using?

Start a few containers:

```bash
docker run -d --name monitor-1 busybox sh -c "while true; do date; sleep 1; done"
docker run -d --name monitor-2 busybox sh -c "while true; do date; sleep 1; done"
```

**Watch live resource usage:**

```bash
docker stats
```

📊 You'll see a live dashboard showing CPU %, memory usage, network I/O, and more!

Press `Ctrl+C` to exit.

Stats for a specific container:

```bash
docker stats monitor-1
```

💡 This is great for spotting containers that are consuming too many resources.

Clean up:

```bash
docker stop monitor-1 monitor-2
docker rm monitor-1 monitor-2
```

#### Challenge 4: Copy Files Between Host and Container

Sometimes you need to get files into or out of a container. Let's see this in action!

Start a long-running container:

```bash
docker run -d --name file-container busybox sh -c "while true; do sleep 1; done"
```

Copy our famous Berry Blast recipe into the container:

```bash
docker cp smoothies/berry_blast.txt file-container:/berry_blast.txt
```

Verify it's there:

```bash
docker exec file-container cat /berry_blast.txt
```

✅ You should see the berry blast recipe!

Now let's modify the recipe inside the container - add some extra boost:

```bash
docker exec file-container sh -c "echo 'Protein Powder' >> /berry_blast.txt"
```

Check what changed:

```bash
docker exec file-container cat /berry_blast.txt
```

You'll see "Protein Powder" has been added to make it an extra power smoothie!

Copy the modified recipe back to your host:

```bash
docker cp file-container:/berry_blast.txt ./berry_blast_modified.txt
```

Compare the two files side by side. You can use `diff` or just `cat` them.

💡 `docker cp` works even if the container is stopped! Try it:

```bash
docker stop file-container
docker cp file-container:/berry_blast.txt ./berry_blast_from_stopped.txt
cat berry_blast_from_stopped.txt
```

Clean up:

```bash
docker rm file-container
rm berry_blast_modified.txt berry_blast_from_stopped.txt
```

### 🎓 What You've Learned

Congratulations! You now know how to:

✅ Run containers interactively and in detached mode  
✅ Manage container lifecycle (start, stop, restart)  
✅ View and follow container logs  
✅ Execute commands in running containers  
✅ Name containers for easier management  
✅ Clean up containers and images  
✅ Inspect container details  
✅ Monitor resource usage  
✅ Copy files between the host and containers  

You're ready to start working with real applications in containers!

### 🏆 Summary Cheat Sheet

| Command | Description |
|---|---|
| `docker run <image>` | Create and start a new container |
| `docker run -it <image>` | Run interactively with terminal |
| `docker run -d <image>` | Run in detached (background) mode |
| `docker run --rm <image>` | Auto-remove container after it stops |
| `docker run --name <name> <image>` | Give container a friendly name |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers (including stopped) |
| `docker ps --filter "name=<pattern>"` | Filter containers by name |
| `docker ps --filter "status=<status>"` | Filter containers by status |
| `docker logs <container>` | View container logs |
| `docker logs -f <container>` | Follow logs in real-time (Ctrl+C to exit) |
| `docker exec -it <container> sh` | Open shell in running container |
| `docker exec <container> <command>` | Execute a command in running container |
| `docker stop <container>` | Stop a running container |
| `docker start <container>` | Start a stopped container |
| `docker restart <container>` | Restart a container |
| `docker rm <container>` | Remove a stopped container |
| `docker images` | List images |
| `docker rmi <image>` | Remove an image |
| `docker container prune` | Remove all stopped containers |
| `docker image prune` | Remove unused images |
| `docker inspect <container>` | Show detailed container information |
| `docker inspect --format='{{...}}' <container>` | Extract specific information |
| `docker stats` | Show live resource usage for all containers |
| `docker stats <container>` | Show live resource usage for specific container |
| `docker cp <file> <container>:<path>` | Copy file from host to container |
| `docker cp <container>:<path> <file>` | Copy file from container to host |

💡 You can use either container names or IDs with most commands.

## Building Our First Image 🧱

So far we've been using images that others have built (hello-world, busybox, rancher/cowsay).
Now it's time to build our own! We'll start with something very simple.

We have prepared a file called `Dockerfile_Helloworld`. Let's look at it:

```dockerfile
FROM alpine:latest
ENTRYPOINT ["echo"]
CMD ["Hello Docker World"]
```

**What does this mean?**
* `FROM alpine:latest`: Start with a lightweight Linux base image (Alpine).
* `ENTRYPOINT ["echo"]`: This image is designed to run the `echo` command.
* `CMD ["Hello Docker World"]`: If no arguments are provided, use this default message.

Let's turn this recipe into an actual image. We'll tag it with the name `ais-hello-world`.

```bash
docker build -t ais-hello-world -f Dockerfile_Helloworld .
```

* `-t ais-hello-world`: Give the image a name (tag).
* `-f Dockerfile_Helloworld`: Use our specific file (default is `Dockerfile`).
* `.`: Look for files in the current directory (context).

Now run our newly crafted image:

```bash
docker run ais-hello-world
```

You should see:
`Hello Docker World`


Because we used `ENTRYPOINT` and `CMD`, we can override the message by passing arguments!

```bash
docker run ais-hello-world "I am a Docker Master"
```

You should see:
`I am a Docker Master`

**Why did that happen?**
When you provide arguments after the image name, they replace the `CMD` part but keep the `ENTRYPOINT`.
So effectively, Docker ran: `echo "I am a Docker Master"` instead of `echo "Hello Docker World"`.

## Smoothies in a Box 📦

Now for the real deal. We're going to containerize our Power Smoothie Maker application.

Create a new file named `Dockerfile` (no extension) in your project root. We'll build it piece by piece.

Paste these commands line by line:

```dockerfile
FROM debian:bookworm-slim
```

We're using Debian 12 (Bookworm) as our OS. "slim" means it's stripped down to save space. 
It's like buying an unfurnished apartment.

🛡️**Security Bonus:** A smaller image also means better security! Fewer installed packages mean 
fewer potential vulnerabilities (a smaller "attack surface") that hackers can exploit.

```dockerfile
# Set the working directory
WORKDIR /app
```

This creates a directory called `/app` inside the container and moves us into it. 
All future commands will run here. It's like doing `mkdir /app` and `cd /app` in one go.

**Installing Tools**

We need `uv` to manage our Python dependencies. But first, we need `curl` to download it. Add these lines:

```dockerfile
# Install curl and ca-certificates to be able to download uv
RUN apt-get update && apt-get install -y curl ca-certificates && rm -rf /var/lib/apt/lists/*
```

This updates the package manager list, installs `curl` (for downloading) and `ca-certificates` (for secure connections), 
and then immediately cleans up the cache to keep the image small.

Now install `uv` and add it to the path:

```dockerfile
# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh
# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"
```

We download and run the installer script for `uv`, then update the `PATH` environment variable 
so the system knows where to find the `uv` executable. Remember that you've done exactly the same 
in our last sessions when we've installed `uv` on our machines ? 

**Bringing in the Code**

Now let's get our application files into the container.

```dockerfile
# Copy the application code
COPY . .
```

This copies **everything** from your current folder on your computer (the first `.`) into the current folder 
inside the image (the second `.`, which is `/app`).

**Installing Dependencies**

We have the code, but we need the Python libraries.

```dockerfile
# Install dependencies
RUN uv sync --frozen
```

`uv` reads our `uv.lock` file and installs exactly the versions of the libraries we need. 
`--frozen` ensures it doesn't try to update them, ensuring reproducibility. Remember that 
you've done exactly the same in our last sessions when built our CI pipeline ?

**The Launch Command**

Finally, tell Docker what to do when the container starts.

```dockerfile
# Set the entrypoint
ENTRYPOINT ["uv", "run", "main.py"]
```

This tells Docker: "When you start, execute `uv run main.py`". You should actually be very
familiar with this command after our previous sessions 😉!

### Build and Run

Now let's build the image for our smoothie maker!

```bash
docker build -t ais-smoothie-maker .
```

And run it:

```bash
docker run --rm ais-smoothie-maker berry_blast.txt
```

⚠️ The smoothie maker was changed for this session in order to require the name of the recipe file 
in the `./smoothies` directory as an argument. Therefore you have to pass `berry_blast.txt` to it.

### 🚀 Level Up

Finished early? Let's explore what's actually inside your container image!

#### Challenge: The Hidden Bloat

Let's peek inside the container we just built and see what files were copied.

First, start a shell inside the container:

```bash
docker run -it --rm ais-smoothie-maker sh
```

Wait... the container starts and exits immediately! That's because we set `ENTRYPOINT` to run `main.py`. We need to override it.

```bash
docker run -it --rm --entrypoint sh ais-smoothie-maker
```

Now you're inside! Let's explore:

```sh
ls -la
```

😱 Look at all those files! You'll see:
- `.git` - The entire Git history (we don't need this in production!)
- `__pycache__` - Python cache files (generated at runtime anyway)
- `.idea` - Your IDE settings (definitely not needed)
- `README.md` - Documentation (not needed to run the app)
- `test_*.py` - Test files (not needed in production)
- Maybe even `.DS_Store` if you're on Mac

**Why is this a problem?**
- 📦 **Larger images** = Slower downloads and deployments
- 🔒 **Security risk** = More files mean more potential vulnerabilities or leaked secrets
- 💾 **Waste** = Storing and transferring unnecessary data

Exit the container:

```sh
exit
```

**The Solution: `.dockerignore`**

Just like `.gitignore` tells Git which files to ignore, `.dockerignore` tells Docker which files NOT to copy!

Create a file called `.dockerignore` in your project root with this content:

```
# Python
__pycache__/
*.py[cod]
*.so
.Python
.venv/
venv/
.pytest_cache/

# Git
.git/
.gitignore
.github/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Project specific
work/
tmp/
TODO
README.md
test_*.py

# OS
.DS_Store
Thumbs.db

# Docker
.dockerignore
Dockerfile*
```

**What does this do?**
- Excludes Python cache and virtual environments
- Keeps Git history out of the image
- Removes IDE configuration files
- Blocks test files from production
- Filters out OS-specific junk files

Now rebuild the image:

```bash
docker build -t ais-smoothie-maker .
```

And inspect it again:

```bash
docker run -it --rm --entrypoint sh ais-smoothie-maker
ls -la
```

🎉 Much cleaner! Only the essential files made it into the container.

💡 **Best Practice:** Always create a `.dockerignore` file for your Docker projects, just like 
you create a `.gitignore` for Git!  

## Production Ready Smoothies in a Box 📦

Our first Dockerfile works, but it's not optimized for production. 
Let's build a better version using **multi-stage builds**.

**What's the problem with our current Dockerfile?**
- We install `curl` and `ca-certificates` just to download `uv`, but we don't need them at runtime
- The final image contains build tools we don't need in production
- The image is larger than it needs to be

**The solution: Multi-stage builds!**

Multi-stage builds let us:
1. Use one stage to **build** and install everything
2. Use a second stage for **runtime** that only contains what's needed to run the app
3. Copy just the compiled/installed artifacts from the builder stage

Let's create `Dockerfile_Clean`. We'll build it step by step.

**Build Arguments**

Start with a build argument so we can easily change the Python version:

```dockerfile
ARG PYTHON_VERSION=3.13
```

This creates a variable we can use throughout the Dockerfile. The variable can also be 
set when we execute `docker build`, which will come in quite handy later.

**The Builder Stage**

This stage will install dependencies.

```dockerfile
# Builder stage: Install dependencies
FROM python:${PYTHON_VERSION}-slim AS builder
```

We're starting the first stage called "builder". 
The `AS builder` names this stage so we can reference it later. 
We use the Python version from our argument.

Set up the working directory:

```dockerfile
WORKDIR /app
```

Install tools we need to build:

```dockerfile
# Install curl for uv
RUN apt-get update && apt-get install -y curl
```

We still need `curl` to download `uv`. 
Notice we don't install `ca-certificates` here because the Python image already includes them!
We also do not clean up anymore because this is a builder stage - we will discard it later anyway.

Install `uv`:

```dockerfile
# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"
```

Now here's something different - copy only the files needed for dependency installation:

```dockerfile
# Copy project files needed for dependency installation
COPY pyproject.toml uv.lock .python-version ./
```

We're NOT copying everything! We only copy the files that define our dependencies. 
This enables better **layer caching** - if our code changes but dependencies don't, 
Docker can reuse this layer, which leads to way faster builds!

Install dependencies:

```dockerfile
# Install dependencies (creates .venv with Python and packages)
RUN uv sync --frozen
```

**The Runtime Stage**

Now for the magic - the second stage that creates our final, lean image:

```dockerfile
# Runtime stage: Clean image with only runtime dependencies
FROM python:${PYTHON_VERSION}-slim
```

We start fresh with a clean Python image. This stage won't have `curl` or any build tools!

```dockerfile
WORKDIR /app
```

Copy the installed Python environment from the builder stage:

```dockerfile
# Copy Python environment and application from builder
COPY --from=builder /app/.venv /app/.venv
```

The magic line! `--from=builder` copies files from the first stage. We get the fully 
installed Python environment without any of the build tools.

Copy only the application code we need:

```dockerfile
# Copy application code
COPY main.py ./
COPY smoothies ./smoothies
```

We're selective - only copy the files needed to run the app. No tests, no docs, no Git history!

Set the entrypoint:

```dockerfile
# Set the entrypoint
ENTRYPOINT ["/app/.venv/bin/python", "main.py"]
```

Note that we use the `python` which was installed by `uv` into our virtual environment 
with all dependencies installed.

### Build and Compare

Build the production-ready image:

```bash
docker build -t ais-smoothie-maker-clean -f Dockerfile_Clean .
```

Let's compare the two images:

```bash
docker images | grep ais-smoothie-maker
```

You should see `ais-smoothie-maker-clean` is smaller! 

Test that it works:

```bash
docker run --rm ais-smoothie-maker-clean berry_blast.txt
```

### Inspect the Clean Image

Let's see how lean this image is:

```bash
docker run -it --rm --entrypoint sh ais-smoothie-maker-clean
```

Inside the container:

```sh
ls -la
which curl
```

Notice:
- Only `main.py` and `smoothies/` directory are present
- `curl` is not found (we don't need it at runtime!)
- The `.venv` contains just what we need

Exit:

```sh
exit
```

**Why is this better?**
- ⚡ **Smaller image** = Faster deployments
- 🔒 **More secure** = Fewer tools means smaller attack surface
- 🎯 **Cleaner** = Only runtime dependencies
- 📦 **Better caching** = Dependency layer is cached separately from code

💡 **Production Tip:** Always use multi-stage builds for production images!

### 🚀 Level Up: Advanced Docker Techniques

#### Challenge 1: Dynamic Python Version

Remember the `ARG PYTHON_VERSION=3.13` at the top of `Dockerfile_Clean`? Let's use it!

We have a `.python-version` file in our project. Let's read it and pass it to Docker at build time.

First, check what's in the file:

```bash
cat .python-version
```

Now build the image using this version:

```bash
docker build -t ais-smoothie-maker-clean \
  --build-arg PYTHON_VERSION=$(cat .python-version) \
  -f Dockerfile_Clean .
```

**What's happening here?**
- `--build-arg PYTHON_VERSION=$(cat .python-version)` passes the Python version to the Dockerfile's ARG

Check your images:

💡 **Production Tip:** Using build args makes your Dockerfiles flexible and reusable across different environments!

#### Challenge 2: Security Scanning with Docker Scout

Docker Scout helps you find security vulnerabilities in your images.

**Scan our image:**

```bash
docker scout cves ais-smoothie-maker-clean
```

You'll see a report listing:
- 🔴 Critical vulnerabilities
- 🟠 High severity issues
- 🟡 Medium and low severity issues
- The packages they come from

**View a quick summary:**

```bash
docker scout quickview ais-smoothie-maker-clean
```

This gives you a high-level security score for each image.

💡 **Security Tip:** Always scan your production images for vulnerabilities! Integrate Docker Scout into your CI/CD pipeline to catch issues early.

**Bonus: Get recommendations**

Want to see how to fix vulnerabilities?

```bash
docker scout recommendations ais-smoothie-maker-clean
```

Docker Scout will suggest:
- Base image updates
- Package version upgrades
- Best practices for security

🎯 **Real-world insight:** In production environments, security scanning is mandatory. 
Multi-stage builds combined with minimal base images (like `-slim`) dramatically reduce your 
security footprint!

## Sharing Images via GitHub Container Registry 📦

Now that we have a great image, let's share it! We'll use **GitHub Container Registry (GHCR)** to store our image so others (or your production servers) can pull and use it.

**👥 Pair Work Alert:** In this section, you'll work together:
- **Student A** (the "Publisher") will push the image to GHCR
- **Student B** (the "Consumer") will pull and run their partner's image

This mirrors real-world team collaboration where developers share containers!

**What is GHCR?**

GitHub Container Registry is a package registry service that lets you store and manage Docker images. It's:
- 🆓 Free for public repositories
- 🔐 Integrated with GitHub authentication
- 🚀 Fast and reliable
- 📦 Lives alongside your code

**Why not Docker Hub?**

Both work great! We use GHCR because:
- It's already integrated with GitHub (where your code is)
- Same authentication tokens work for code and containers
- Great for CI/CD workflows with GitHub Actions

### Part 1: Student A - Publishing the Image 📤

**Student A**, follow these steps to push your image.

#### Authentication

First, you need to authenticate Docker with GHCR. You'll need a GitHub Personal Access Token (PAT).

**Create a Personal Access Token:**

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) (https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name like "Docker GHCR Access"
4. Select scopes:
   - ✅ `write:packages` (upload images)
   - ✅ `read:packages` (download images)
   - ✅ `delete:packages` (delete images - optional)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

**Login to GHCR:**

```bash
echo "YOUR_TOKEN" | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
```

Replace:
- `YOUR_TOKEN` with your actual token
- `YOUR_GITHUB_USERNAME` with your GitHub username

You should see: `Login Succeeded`

#### Tagging for GHCR

GHCR images follow a specific naming convention:

```
ghcr.io/USERNAME/IMAGE_NAME:TAG
```

Let's tag our clean production image:

```bash
docker tag ais-smoothie-maker-clean ghcr.io/YOUR_GITHUB_USERNAME/ais-smoothie-maker:latest
```

Let's also tag it with a version:

```bash
docker tag ais-smoothie-maker-clean ghcr.io/YOUR_GITHUB_USERNAME/ais-smoothie-maker:1.0.0
```

Check your images:

```bash
docker images | grep ais-smoothie-maker
```

You should see your image with both the local name and the GHCR tags.

**Tagging best practices:**
- `latest` - Always points to the most recent stable version
- `1.0.0` - [Semantic versioning](https://semver.org/) for specific releases
- `main` or `dev` - Tags for specific branches
- `pr-123` - Tags for pull requests during testing

#### Pushing to GHCR

Now push your image to GHCR:

```bash
docker push ghcr.io/YOUR_GITHUB_USERNAME/ais-smoothie-maker:latest
docker push ghcr.io/YOUR_GITHUB_USERNAME/ais-smoothie-maker:1.0.0
```

You'll see Docker uploading the layers. Since both tags point to the same image, the second push will be fast 
(layers are already uploaded).

**Verify it's there:**

1. Go to your GitHub profile 
2. Click "Packages" tab (https://github.com/YOUR_GITHUB_USERNAME?tab=packages)
3. You should see `ais-smoothie-maker`!

#### Making the Package Public

By default, packages are private. Let's make it public so your partner can pull it:

1. On GitHub, go to your package page
2. Click "Package settings" (bottom right)
3. Scroll down to "Danger Zone"
4. Click "Change visibility" → "Public"
5. Type the package name to confirm

✅ **Tell Student B:** Share your GitHub username so they can pull your image!

### Part 2: Student B - Pulling and Running 📥

**Student B**, now it's your turn! You'll pull and run Student A's image.

Get Student A's GitHub username (let's call it `PARTNER_USERNAME`).

#### Pull from GHCR

Now pull Student A's image:

```bash
docker pull ghcr.io/PARTNER_USERNAME/ais-smoothie-maker:latest
```

Watch as Docker downloads the layers from GHCR! You're getting the exact same image Student A built.

**Verify it's there:**

```bash
docker images | grep PARTNER_USERNAME
```

#### Run Your Partner's Image

Now run it:

```bash
docker run --rm ghcr.io/PARTNER_USERNAME/ais-smoothie-maker:latest berry_blast.txt
```

🎉 You just ran your partner's containerized application! This is the power of containers - **"Build once, run anywhere"**!


## Automating Docker Builds with CI 🤖

So far, you've been building Docker images manually on your local machine. But what if you could 
automatically build and publish a new Docker image every time you push code to GitHub? That's exactly what we'll do now!

We'll extend our existing CI workflow to automatically:
1. Build a Docker image
2. Push it to GitHub Container Registry (GHCR)
3. Tag it with `latest` and a version number

### Open Your CI Workflow File

Open `.github/workflows/ci.yml` in your editor. You should already be familiar with the contents 
of this file from our previous sessions.

### Add the `build-and-push` Job

At the end of your workflow file, **after** the `scan` job, add a new job. Copy this entire block:

```yaml
  build-and-push:
    name: Build & Push Docker Image
    runs-on: ubuntu-latest
    needs: [test, scan]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    permissions:
      packages: write
    
    steps:
      - uses: actions/checkout@v4

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Read Python version
        id: python-version
        run: echo "version=$(cat .python-version)" >> $GITHUB_OUTPUT

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./Dockerfile_Clean
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:v${{ github.run_number }}
          build-args: |
            PYTHON_VERSION=${{ steps.python-version.outputs.version }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Understanding What You Just Added

Let's break down what the parts that are new to you do:

#### Dependencies and Conditions
```yaml
  needs: [test, scan]
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
```
- `needs`: This job only runs AFTER `test` and `scan` complete successfully
- `if`: Only run when pushing to the `main` branch (not on pull requests or other branches)

**Why?** You don't want to publish every single commit from every branch. Only tested, approved 
code from `main` should get published!

#### Permissions
```yaml
  permissions:
    packages: write
```
This gives the workflow permission to upload packages (Docker images) to GitHub Container Registry.

#### Login to GHCR
```yaml
    - name: Log in to GitHub Container Registry
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
```
Logs Docker into GHCR so it can push images.

`${{ github.actor }}`: Automatically uses the GitHub username that triggered the workflow

`${{ secrets.GITHUB_TOKEN }}`: You are already familiar with this one!

#### Read Python Version
```yaml
    - name: Read Python version
      id: python-version
      run: echo "version=$(cat .python-version)" >> $GITHUB_OUTPUT
```
Reads the Python version from your `.python-version` file and stores it as an output.

`id: python-version` - Gives this step a unique ID so we can reference its output later

`GITHUB_OUTPUT` is a special file that GitHub Actions provides to each step in a workflow. 
It's used to pass data between steps within the same job.

How it works:
1. GitHub creates a file for each job and sets the path in the `$GITHUB_OUTPUT` environment variable
2. You write to it using the format: `name=value`
3. Later steps can read the values using: `${{ steps.<step-id>.outputs.<name> }}`

**Why?** Our Dockerfile uses a Python version argument, and we want to use the same version we're developing with!

#### Set Up Docker Buildx
```yaml
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
```
Sets up Docker Buildx, which is an enhanced Docker build tool. It supports:
- Building for different platforms (AMD64, ARM, etc.)
- Advanced caching
- Better performance

#### Step 5: Build and Push the Image
```yaml
    - name: Build and push Docker image
      uses: docker/build-push-action@v6
      with:
        context: .
        file: ./Dockerfile_Clean
        push: true
        tags: |
          ghcr.io/${{ github.repository }}:latest
          ghcr.io/${{ github.repository }}:v${{ github.run_number }}
        build-args: |
          PYTHON_VERSION=${{ steps.python-version.outputs.version }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

Let's break down each parameter:

- `context: .` - The build context (current directory). Same as you specified in `docker build .`
- `file`: ./Dockerfile_Clean` - Which Dockerfile to use
- `push: true` - Automatically push after building
- `tags: ...:latest` - Always points to the most recent build
- `tags: ...:v<number>` - A unique version number (GitHub automatically increments `run_number`)
- `build-args:` - Passes the Python version to the Dockerfile
- `cache-from/cache-to:` - Uses GitHub's cache to speed up builds

**Example:** If this is your 42nd workflow run, it will create:
- `ghcr.io/YOUR_USERNAME/YOUR_REPO:latest`
- `ghcr.io/YOUR_USERNAME/YOUR_REPO:v42`

### Commit and Push

Save your changes, commit and push to GitHub.

### Watch It Run! 🎬

1. Go to your GitHub repository
2. Click the **"Actions"** tab
3. You should see your workflow running
4. Click on the workflow run to see details
5. Watch as it:
   - ✅ Runs tests
   - ✅ Runs security scans  
   - ✅ Builds your Docker image
   - ✅ Pushes it to GHCR

This might take a few minutes (especially the first time).

### Verify Your Published Image

Once the workflow completes, check your packages and verify that it works using the 
knowledge that you already gathered in the last section about GHCR.

### What Just Happened?

Let's trace the full journey:

1. 👨‍💻 You wrote code and pushed to `main`
2. 🤖 GitHub Actions automatically started
3. ✅ It ran all your tests (ensuring quality)
4. 🔒 It ran security scans (ensuring safety)  
5. 🐳 It built a Docker image with your code
6. 📤 It pushed the image to GHCR with proper tags
7. 🌍 Anyone in the world can now pull and run your code!

**This is the power of CI/CD!** Your code goes from your laptop to production-ready containers automatically.