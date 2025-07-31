# src/ldumpj/models.py (create this new file)
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, Any, List, Union, Self, Tuple
from enum import StrEnum
from sys import exit

class EndPoint(BaseModel):
    port: int
    active: bool
    managed: bool
    reset: bool
    hide: bool
    watching: bool
    
class ProgramType(StrEnum):
    PLAIN = "Plain"
    DAEMON = "LaunchDaemon"
    XPC = "XPC"

class ServiceDomain(StrEnum):
    SYSTEM = "system"
    USER = "user"
    GUI = "gui"
    PID = "pid"
    OTHER = "other"

class LauchctlService(BaseModel):
    
    def __init__(self,**kwargs):
        try:
            super().__init__(**kwargs)
        except TypeError as e:
            print(kwargs)
            exit(0)
    
    active_count: Optional[int] = Field(None, alias="active count")
    
    path: Optional[str] = None
    type: Optional[str] = None
    state: Optional[str] = None
    
    program: Optional[str] = None
    arguments: Optional[List[str]] = []
    
    spawn_type: Optional[str] = Field(None, alias="spawn type")
    last_exit_code: Optional[str] = Field(None, alias="last exit code")
    
    default_environment: Optional[Dict[str, Union[str,int]]] = Field(None, alias="default environment")
    environment: Optional[Dict[str, Union[str,int]]] = None
    
    domain: Optional[str] = None
    endpoints: Optional[Union[Dict[str, EndPoint],List[str]]] = None
    services: Optional[List[str]] = None

    
    runs: Optional[int] = None
    pid: Optional[int] = None
    forks: Optional[int] = None
    execs: Optional[int] = None

    initialized: Optional[bool] = None
    trampolined: Optional[bool] = None
    started_suspended: Optional[bool] = Field(None, alias="started suspended")
    proxy_started_suspended: Optional[bool] = Field(None, alias="proxy started suspended")
    
    jetsam_priority: Optional[int] = Field(None, alias="jetsam priority")
    jetsam_memory_limit_active_soft: Optional[str] = Field(None, alias="jetsam memory limit (active, soft)")
    jetsam_memory_limit_inactive_soft: Optional[str] = Field(None, alias="jetsam memory limit (inactive, soft)")
    jetsamproperties_category: Optional[str] = Field(None, alias="jetsamproperties category")
    jetsam_thread_limit: Optional[int] = Field(None, alias="jetsam thread limit")

    properties: List[str] = None
    
    class Config:
        populate_by_name = True # Allow parsing by field name and alias
        extra = "allow" # Ignore extra fields not defined in the model. Change to "forbid" for strict validation.

    @model_validator(mode="before")
    @classmethod
    def properties_to_list(cls,object : Dict[str,str]) -> List[str]:
        if "properties" not in object:
            object["properties"] = []
            return object
    
        values = object["properties"]
        if values is None:
            object["properties"] = []
            return object
    
        object["properties"] = [prop.strip() for prop in values.split("|")]
        return object
    
    @model_validator(mode="after")
    def fix_program_and_arguments(self) -> Self:
        if not self.program and not self.arguments:
            return self
        
        if self.program is None:
            self.program = self.arguments[0]
            self.arguments = self.arguments[1:]
 
        return self        