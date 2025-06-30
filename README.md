
# `ldumpj`: Bridging `launchctl` Output to Processable JSON

While `launchctl` is an essential tool for managing macOS services, its output is notoriously difficult for programs to parse. `ldumpj` is a command-line utility that tackles this challenge head-on by converting the human-readable output of `launchctl` into structured JSON. Internally, we parse the preprocessed output with a LALR grammer and transform the resulting AST into python objects.

> **Important Note:** As `launchctl` itself states, its output is not intended for programmatic parsing and is subject to change across macOS releases. This tool aims to provide a useful bridge for automation, but its stability is dependent on the consistency of `launchctl`'s output format.

---

## Why Use This Tool?

Automating tasks that involve `launchctl dumpstate` or `launchctl print` can be a headache if you wish to extrat complex information. Traditional scripting often relies on `grep`, which does the job for simple tasks. By converting to **JSON**, `launchctl-dumpstate-json` allows you to:

* **Easily process `launchctl` data** with other scripting languages or tools.
* **Integrate `launchctl` information** into monitoring systems or dashboards.
* **Simplify complex automation workflows** that depend on `launchctl` states.

---

## Installation

For now, use `uv` to directly use the package, as you only need to use it likely once. 

```bash
launchctl dumpstate | uvx git+https://github.com/bluuuk/launchctl-dumpstate-json 
```
Otherwise, use `git clone https://github.com/bluuuk/launchctl-dumpstate-json` and then use `uv run ldumpj` 

-----

## Usage

```
usage: ldumpj [-h] [-i INPUT] [-o OUTPUT] [-p]

Parses the output of `launchctl dumpstate` and `launchctl print` into json

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file, defaults to stdin
  -o OUTPUT, --output OUTPUT
                        Output file, defaults to stdout
  -p, --pretty          JSON indentation for human-readable output
```

-----

## Examples

`ldumpj` supports both `launchctl dumpstate` (for all services) and `launchctl print {target}` (for a specific service).

### Parsing a Specific Service

Let's say you want to get detailed information about the `com.apple.runningboardd` service in JSON format:

```bash
❯ launchctl print system/com.apple.runningboardd | uv run ldumpj -p
{
 "system/com.apple.runningboardd": {
  "active count": 3,
  "path": "/System/Library/LaunchDaemons/com.apple.runningboardd.plist",
  "type": "LaunchDaemon",
  "state": "running",
  "program": "/usr/libexec/runningboardd",
  "default environment": {
   "PATH": "/usr/bin:/bin:/usr/sbin:/sbin"
  },
  "environment": {
   "MallocSpaceEfficient": 1,
   "XPC_SERVICE_NAME": "com.apple.runningboardd"
  },
  "domain": "system",
  "minimum runtime": 1,
  "base minimum runtime": 1,
  "exit timeout": 5,
  "runs": 1,
  "pid": 170,
  "immediate reason": "ipc (mach)",
  "forks": 0,
  "execs": 1,
  "initialized": 1,
  "trampolined": 1,
  "started suspended": 0,
  "proxy started suspended": 0,
  "last exit code": "(never exited)",
  "endpoints": {
   "com.apple.runningboard": {
    "port": 69891,
    "active": 1,
    "managed": 1,
    "reset": 0,
    "hide": 0,
    "watching": 0
   },
   "com.apple.runningboard.resource_notify": {
    "port": 69639,
    "active": 1,
    "managed": 1,
    "reset": 0,
    "hide": 0,
    "watching": 0
   }
  },
  "spawn type": "adaptive (6)",
  "jetsam priority": 180,
  "jetsam memory limit (active, soft)": "50 MB",
  "jetsam memory limit (inactive, soft)": "50 MB",
  "jetsamproperties category": "daemon",
  "jetsam thread limit": 32,
  "cpumon": "default",
  "exponential throttling grace limit": 10,
  "job state": "running",
  "probabilistic guard malloc policy": {
   "activation rate": "1/1000",
   "sample rate": "1/0"
  },
  "properties": "supports transactions | supports pressured exit | system service | exponential throttling | tle system"
 }
}
```

### Combining with `jq` for Powerful Filtering

The true power of JSON output shines when combined with tools like `jq`. For instance, to get a list of all loaded services:

```bash
❯ launchctl dumpstate | uv run ldumpj -p | jq 'keys'
```

-----

## Performance

Here's how `ldumpj` performs on various test `dumpstate` inputs:

```bash
❯ for i in test/*; do time uv run ldumpj -i "$i" -o /dev/null ; done
uv run ldumpj -i "$i" -o /dev/null  1.56s user 0.04s system 99% cpu 1.609 total
uv run ldumpj -i "$i" -o /dev/null  1.04s user 0.02s system 99% cpu 1.073 total
uv run ldumpj -i "$i" -o /dev/null  1.38s user 0.03s system 99% cpu 1.415 total
```

-----

## Future Enhancements

Here are some features planned for future releases:

- [ ] Enhance performance and memory efficiency for very large `launchctl dumpstate` outputs. But for now, it should be fast enough
- [ ] Improved resiliency: Further refine the parsing logic to handle unexpected variations in `launchctl` output more gracefully.
- [ ] Improve packaging

-----

License: MIT Lukas Boschanski