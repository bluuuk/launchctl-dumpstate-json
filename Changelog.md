# Mac0S 26 type changes 

```
❯ rg "type = \w+" macos26.txt | tr -d "\t" | sort -u
spawn type = adaptive (6)
spawn type = app (1)
spawn type = app (nonui) (2)
spawn type = background (5)
spawn type = daemon (3)
spawn type = interactive (4)
type = datagram
type = Extension
type = jetsam
type = LaunchAgent
type = LaunchAngel
type = LaunchDaemon
type = login
type = pid
type = resource
type = stream
type = Submitted
type = system
type = user
type = XPCService
```

As it is quite unpreditcable to deal with the `type` attribute, I will just omit the enum, as it changed quite much in comparision with the last macOS:

```
❯ rg "type = \w+" macOS15-5.v1.txt | tr -d "\t" | sort -u
spawn type = adaptive (6)
spawn type = app (1)
spawn type = background (5)
spawn type = daemon (3)
spawn type = interactive (4)
type = datagram
type = Extension
type = LaunchAgent
type = LaunchDaemon
type = login
type = pid
type = stream
type = Submitted
type = system
type = user
type = XPCService
```