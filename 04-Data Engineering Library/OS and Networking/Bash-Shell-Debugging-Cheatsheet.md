# Bash And Shell Debugging Cheatsheet

## How To Use This Note
These commands are meant for fast production debugging, interview recall, and local investigation. The goal is not to memorize every flag, but to know which tool to reach for first.

## Files And Directories
- `pwd` -> show current directory
- `ls -lah` -> list files with permissions, size, and hidden files
- `du -sh *` -> show directory sizes in the current path
- `df -h` -> show filesystem free space
- `stat <file>` -> show file metadata and timestamps
- `file <file>` -> identify file type

## Search And Inspect
- `rg "<pattern>" <path>` -> fast recursive text search
- `rg --files <path>` -> list files when you know the target area
- `find <path> -maxdepth 2 -type f` -> shallow file discovery
- `head -n 50 <file>` -> first lines
- `tail -n 100 <file>` -> last lines
- `tail -f <file>` -> follow a growing log
- `less <file>` -> open large files safely
- `wc -l <file>` -> count lines
- `sort <file> | uniq -c | sort -nr` -> frequency summary

## Processes
- `ps -ef` -> list running processes
- `ps -ef | rg "<name>"` -> find a process by name
- `pgrep -af "<name>"` -> search process id and full command
- `top` -> live CPU and memory view
- `htop` -> friendlier live process view if installed
- `pstree -p` -> parent and child process tree
- `lsof -p <pid>` -> open files for a process
- `lsof <file>` -> which process has a file open

## CPU And Memory
- `free -h` -> memory usage summary
- `vmstat 1` -> CPU, memory, paging, and runnable queue every second
- `pidstat 1` -> per-process CPU and IO stats if installed
- `top -H -p <pid>` -> thread-level CPU for a process
- `cat /proc/<pid>/status` -> process memory and thread summary
- `cat /proc/meminfo` -> low-level memory stats

## Disk And IO
- `iostat -xz 1` -> disk utilization and latency if installed
- `iotop` -> live per-process disk IO if installed
- `lsblk` -> block device layout
- `mount` -> mounted filesystems
- `dmesg | tail -n 50` -> recent kernel messages

## Networking
- `ss -ltnp` -> listening TCP sockets with process info
- `ss -tan` -> all TCP connections
- `ss -s` -> socket summary
- `ip addr` -> network interfaces and IPs
- `ip route` -> routing table
- `ping <host>` -> basic reachability and RTT
- `nslookup <host>` -> DNS lookup
- `dig <host>` -> detailed DNS lookup if installed
- `curl -I <url>` -> fetch response headers
- `curl -v <url>` -> verbose HTTP request
- `traceroute <host>` -> path to destination if installed

## Logs And System State
- `journalctl -xe` -> recent systemd errors if available
- `journalctl -u <service>` -> logs for a systemd service
- `journalctl -f` -> follow system logs
- `uptime` -> load average and uptime
- `who` -> logged-in users
- `env | sort` -> environment variables

## Containers And Runtime Environments
- `docker ps` -> running containers
- `docker logs <container>` -> container logs
- `docker stats` -> live container resource usage
- `kubectl get pods` -> pod status
- `kubectl describe pod <pod>` -> pod events and details
- `kubectl logs <pod>` -> pod logs

## Common Debugging Pipelines
### Find A Process And Inspect It
```bash
pgrep -af "java|python|node"
top -H -p <pid>
lsof -p <pid>
```

### Check Whether A Port Is Listening
```bash
ss -ltnp | rg ":8080"
curl -v http://localhost:8080/health
```

### Follow Errors In A Log
```bash
tail -f app.log | rg "ERROR|WARN|Exception"
```

### Find Large Directories
```bash
du -sh *
df -h
```

### See Whether The System Is Under Pressure
```bash
uptime
vmstat 1
free -h
ss -s
```

## Interview Angle
- `ss` is the modern replacement for many `netstat` use cases.
- `vmstat` is a compact first-pass tool because it shows runnable pressure, memory activity, and swap behavior together.
- `lsof` is often the quickest way to answer "who is using this file or port?"
- `tail -f`, `rg`, and `journalctl` cover a large percentage of real debugging sessions.

## Related
- [[04-Data Engineering Library/OS and Networking/OS-Networking-Cheatsheet.md]]
- [[04-Data Engineering Library/OS and Networking/OS-CPU-Scheduling-Latency.md]]
- [[04-Data Engineering Library/OS and Networking/Networking-TCP-Connection-Lifecycle.md]]
