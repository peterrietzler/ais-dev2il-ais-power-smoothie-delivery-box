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

