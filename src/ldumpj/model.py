# src/ldumpj/models.py (create this new file)
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional, Dict, Any, List, Union, Self, Tuple
from enum import StrEnum, Enum
from sys import exit

class EndPoint(BaseModel):
    port: str = Field(description="The port number of the endpoint, often in hex.")
    active: bool = Field(description="Whether the endpoint is active.")
    managed: bool = Field(description="Whether the endpoint is managed by launchd.")
    reset: bool = Field(description="Whether the endpoint has been reset.")
    hide: bool = Field(description="Whether the endpoint is hidden.")
    watching: bool = Field(description="Whether launchd is watching the endpoint.")

    @model_validator(mode="before")
    @classmethod
    def port_to_hex(cls,object : Dict[str,str]) -> Dict[str,str]:
        object["port"] = hex(object["port"])[2:]
        return object

        
class Socket(BaseModel):
    model_config = ConfigDict(extra="allow")
    
    sock_type: Optional[str] = Field(None, alias='SockType', description="The socket type, e.g., 'stream', 'dgram'.")
    sock_passive: Optional[bool] = Field(None, alias='SockPassive', description="Whether the socket is passive.")
    sock_node_name: Optional[str] = Field(None, alias='SockNodeName', description="The node name to bind to.")
    sock_service_name: Optional[str] = Field(None, alias='SockServiceName', description="The service name to bind to.")
    sock_family: Optional[str] = Field(None, alias='SockFamily', description="The socket family, e.g., 'IPv4', 'IPv6'.")
    sock_protocol: Optional[str] = Field(None, alias='SockProtocol', description="The socket protocol, e.g., 'TCP', 'UDP'.")
    sock_path_name: Optional[str] = Field(None, alias='SockPathName', description="The path to the socket in the file system.")
    secure_socket_with_key: Optional[str] = Field(None, alias='SecureSocketWithKey', description="A key for secure socket options.")
    sock_path_mode: Optional[int] = Field(None, alias='SockPathMode', description="The mode of the socket path.")
 
 
class ProgramType(str, Enum):
    DAEMON = "LaunchDaemon"
    XPC_SERVICE = "XPCService"
    SUBMITTED = "Submitted"
    SYSTEM = "system"

class ServiceDomain(StrEnum):
    SYSTEM = "system"
    USER = "user"
    GUI = "gui"
    PID = "pid"
    OTHER = "other"

class LauchctlService(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
        use_enum_values = True
    )

    active_count: int = Field(alias="active count", description="The number of active processes for this service.")
    path: Optional[str] = Field("",description="The path to the service's property list file.")
    type: Optional[ProgramType] = Field(None,description="The type of the service.")
    state: Optional[str] = Field("", description="The current state of the service.")
    
    program: Optional[str] = Field("", description="The program to be executed.")
    arguments: Optional[List[str]] = Field([], description="The arguments to pass to the program.")
    
    spawn_type: Optional[str] = Field(None, alias="spawn type", description="The spawn type of the service.")
    last_exit_code: Optional[Union[str, int]] = Field(None, alias="last exit code", description="The last exit code of the service.")
    
    default_environment: Optional[Dict[str, Union[str,int]]] = Field(None, alias="default environment", description="The default environment variables for the service.")
    environment: Optional[Dict[str, Union[str,int,None]]] = Field(None, description="The environment variables for the service.")
    
    domain: Optional[str] = Field(None, description="The domain the service is running in.")
    endpoints: Optional[Union[Dict[str, EndPoint],List[str]]] = Field(None, description="The endpoints exposed by the service.")
    services: Optional[List[str]] = Field(None, description="The services provided by this service.")
    
    runs: Optional[int] = Field(None, description="The number of times the service has run.")
    pid: Optional[int] = Field(None, description="The process ID of the service.")
    forks: Optional[int] = Field(None, description="The number of times the service has been forked.")
    execs: Optional[int] = Field(None, description="The number of times the service has been executed.")

    initialized: Optional[bool] = Field(None, description="Whether the service has been initialized.")
    trampolined: Optional[bool] = Field(None, description="Whether the service has been trampolined.")
    started_suspended: Optional[bool] = Field(None, alias="started suspended", description="Whether the service was started in a suspended state.")
    proxy_started_suspended: Optional[bool] = Field(None, alias="proxy started suspended", description="Whether the proxy was started in a suspended state.")
    
    jetsam_priority: Optional[Union[str, int]] = Field(None, alias="jetsam priority", description="The jetsam priority of the service.")
    jetsam_memory_limit_active_soft: Optional[str] = Field(None, alias="jetsam memory limit (active, soft)", description="The soft active jetsam memory limit.")
    jetsam_memory_limit_inactive_soft: Optional[str] = Field(None, alias="jetsam memory limit (inactive, soft)", description="The soft inactive jetsam memory limit.")
    jetsamproperties_category: Optional[str] = Field(None, alias="jetsamproperties category", description="The jetsam properties category.")
    jetsam_thread_limit: Optional[Union[str, int]] = Field(None, alias="jetsam thread limit", description="The jetsam thread limit.")

    properties: List[str] = Field([], description="A list of properties for the service.")

    # from man launchd.plist
    disabled: bool = Field(False, description="Specifies whether the job is disabled.")
    user_name: Optional[str] = Field(None, alias='UserName', description="The user to run the job as.")
    group_name: Optional[str] = Field(None, alias='GroupName', description="The group to run the job as.")
    run_at_load: bool = Field(False, alias='RunAtLoad', description="Whether to run the job when it is loaded.")
    start_interval: Optional[int] = Field(None, alias='StartInterval', description="The interval in seconds to run the job.")
    start_calendar_interval: Optional[Union[Dict[str, int], List[Dict[str, int]]]] = Field(None, alias='StartCalendarInterval', description="The calendar interval to run the job.")
    queue_directories: Optional[List[str]] = Field(None, alias='QueueDirectories', description="Directories to watch for files.")
    watch_paths: Optional[List[str]] = Field(None, alias='WatchPaths', description="Paths to watch for modifications.")
    time_out: Optional[int] = Field(None, alias='TimeOut', description="The recommended idle timeout in seconds.")
    exit_time_out: int = Field(20, alias='ExitTimeOut', description="The time in seconds to wait before sending SIGKILL.")
    throttle_interval: int = Field(10, alias='ThrottleInterval', description="The interval in seconds to throttle the job.")
    standard_out_path: Optional[str] = Field(None, alias='StandardOutPath', description="Path to the standard output file.")
    standard_error_path: Optional[str] = Field(None, alias='StandardErrorPath', description="Path to the standard error file.")
    working_directory: Optional[str] = Field(None, alias='WorkingDirectory', description="The working directory for the job.")
    root_directory: Optional[str] = Field(None, alias='RootDirectory', description="The root directory for the job.")
    inetd_compatibility: Optional[Dict[str, bool]] = Field(None, alias='inetdCompatibility', description="inetd compatibility options.")
    hard_resource_limits: Optional[Dict[str, int]] = Field(None, alias='HardResourceLimits', description="Hard resource limits.")
    soft_resource_limits: Optional[Dict[str, int]] = Field(None, alias='SoftResourceLimits', description="Soft resource limits.")
    nice: Optional[int] = Field(None, alias='Nice', description="The nice value for the job.")
    process_type: Optional[str] = Field(None, alias='ProcessType', description="The process type.")
    abandon_process_group: bool = Field(False, alias='AbandonProcessGroup', description="Whether to abandon the process group.")
    low_priority_io: bool = Field(False, alias='LowPriorityIO', description="Whether to use low priority I/O.")
    launch_only_once: bool = Field(False, alias='LaunchOnlyOnce', description="Whether to launch the job only once.")
    mach_services: Optional[Dict[str, bool]] = Field(None, alias='MachServices', description="Mach services.")
    sockets: Optional[Dict[str, Union[Socket,List[Any]]]] = Field(None, alias='Sockets', description="Sockets to create.")

    # from xpcservice.plist documentation
    join_existing_session: Optional[bool] = Field(None, alias='JoinExistingSession', description="Whether the service can join an existing session.")
    run_loop_type: Optional[str] = Field(None, alias='RunLoopType', description="The run loop type for the service.")
    
    @model_validator(mode="before")
    @classmethod
    def properties_to_list(cls,object : Dict[str,str]) -> List[str]:
        if "properties" not in object or object["properties"] is None:
            object["properties"] = []
            return object
    
        object["properties"] = [prop.strip() for prop in object["properties"].split("|")]
        return object
    
    @model_validator(mode="after")
    def set_default_daemon_username_root(self) -> Self:
        if self.domain == ServiceDomain.SYSTEM and self.user_name is None:
            self.user_name = "root"
        return self

    @model_validator(mode="after")
    def fix_program_and_arguments(self) -> Self:
        if not self.program and not self.arguments:
            return self
        
        if self.program is None:
            self.program = self.arguments[0]
            self.arguments = self.arguments[1:]
 
        return self        