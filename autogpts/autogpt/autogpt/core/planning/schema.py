import enum
from typing import Optional

from pydantic import BaseModel, Field

from autogpt.core.ability.schema import AbilityResult
from autogpt.core.resource.model_providers.schema import (
    LanguageModelFunction,
    LanguageModelMessage,
)


class LanguageModelClassification(str, enum.Enum):
    """The LanguageModelClassification is a functional description of the model.

    This is used to determine what kind of model to use for a given prompt.
    Sometimes we prefer a faster or cheaper model to accomplish a task when
    possible.

    """

    FAST_MODEL = "fast_model"
    SMART_MODEL = "smart_model"


class LanguageModelPrompt(BaseModel):
    messages: list[LanguageModelMessage]
    functions: list[LanguageModelFunction] = Field(default_factory=list)

    def __str__(self):
        return "\n\n".join(
            f"{m.role.value.upper()}: {m.content}"
            for m in self.messages
        )


class TaskType(str, enum.Enum):
    RESEARCH = "research"
    WRITE = "write"
    EDIT = "edit"
    CODE = "code"
    DESIGN = "design"
    TEST = "test"
    PLAN = "plan"


class TaskStatus(str, enum.Enum):
    BACKLOG = "backlog"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskContext(BaseModel):
    cycle_count: int = 0
    status: TaskStatus = TaskStatus.BACKLOG
    parent: Optional["Task"] = None
    prior_actions: list[AbilityResult] = Field(default_factory=list)
    memories: list = Field(default_factory=list)
    user_input: list[str] = Field(default_factory=list)
    supplementary_info: list[str] = Field(default_factory=list)
    enough_info: bool = False


class Task(BaseModel):
    objective: str
    type: str  # TaskType  FIXME: gpt does not obey the enum parameter in its schema
    priority: int
    ready_criteria: list[str]
    acceptance_criteria: list[str]
    context: TaskContext = Field(default_factory=TaskContext)


# Need to resolve the circular dependency between Task and TaskContext once both models are defined.
TaskContext.update_forward_refs()
