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

# Ignore values that dont have a key value structure

Now, I will just print them to stderr and ignore them.

```
Ignore value `submitted job. ignore execute allowed` in system/com.apple.IOUserDockChannelSerial-0x100000c84
Ignore value `submitted job. ignore execute allowed` in system/NetworkExtension.com.cisco.anyconnect.macos.acsockext.5.1.7.39.5.1.7.39
Ignore value `panic on consecutive crashes (0)` in system/com.apple.kernelmanager_helper
Ignore value `submitted job. ignore execute allowed` in system/com.apple.ftp-proxy
Ignore value `submitted job. ignore execute allowed` in system/com.vmware.DiskHelper
Ignore value `submitted job. ignore execute allowed` in system/com.apple.bcmwlan-0x100000c86
Ignore value `submitted job. ignore execute allowed` in system/com.cisco.secureclient.vpn.service.agent
Ignore value `submitted job. ignore execute allowed` in system/com.vmware.MountHelper
Ignore value `panic on consecutive crashes (0)` in system/com.apple.logd
Ignore value `submitted job. ignore execute allowed` in system/com.vmware.IDHelper
Ignore value `panic on consecutive crashes (0)` in system/com.apple.watchdogd
Ignore value `panic on consecutive crashes (0)` in system/com.apple.kernelmanagerd
```