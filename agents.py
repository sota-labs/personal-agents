from typing import List, Optional, Sequence

from llama_index.core import PromptTemplate
from llama_index.core.agent import ReActAgent
from llama_index.core.agent.react.formatter import (
    ReActChatFormatter,
    get_react_tool_descriptions,
)
from llama_index.core.agent.react.prompts import (
    CONTEXT_REACT_CHAT_SYSTEM_HEADER,
    REACT_CHAT_SYSTEM_HEADER,
)
from llama_index.core.agent.react.types import (
    BaseReasoningStep,
    ObservationReasoningStep,
)
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.tools import BaseTool, ToolOutput
from utils.output_parser import ReActOutputParser
from tools import (
    search_token,
    get_trending_pairs,
    scan_token,
)

from prompts.react import REACT_CHAT_SYSTEM_HEADER_CUSTOM
from LLM.llm_settings_manager import LLMSettingsManager

llm_manager = LLMSettingsManager()
llm = llm_manager.get_llm("gemini", model="models/gemini-2.0-flash")

class CustomReActChatFormatter(ReActChatFormatter):
    """ReAct chat formatter."""

    def __init__(
        self,
        system_header: str = REACT_CHAT_SYSTEM_HEADER,  # default system header
        context: str = "",  # default context (optional)
        **kwargs,
    ):
        """
        Initialize the CustomReActChatFormatter.

        Args:
            system_header (str): The system header template string.
            context (str): Additional context to include in the format.
            **kwargs: Additional keyword arguments to store and use in formatting.
        """
        super().__init__(system_header=system_header, context=context)
        self._kwargs = kwargs

    def format(
        self,
        tools: Sequence[BaseTool],
        chat_history: List[ChatMessage],
        current_reasoning: Optional[List[BaseReasoningStep]] = None,
        **kwargs,
    ) -> List[ChatMessage]:
        """Format chat history into list of ChatMessage."""
        current_reasoning = current_reasoning or []

        format_args = {
            "tool_desc": "\n".join(get_react_tool_descriptions(tools)),
            "tool_names": ", ".join([tool.metadata.get_name() for tool in tools]),
        }

        if self.context:
            format_args["context"] = self.context

        combined_args = {**format_args, **self._kwargs}
        fmt_sys_header = self.system_header.format(**combined_args)
        reasoning_history = []
        for reasoning_step in current_reasoning:
            if isinstance(reasoning_step, ObservationReasoningStep):
                message = ChatMessage(
                    role=MessageRole.USER,
                    content=reasoning_step.get_content(),
                )
            else:
                message = ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=reasoning_step.get_content(),
                )
            reasoning_history.append(message)

        return [
            ChatMessage(role=MessageRole.SYSTEM, content=fmt_sys_header),
            *chat_history,
            *reasoning_history,
        ]

    @classmethod
    def from_defaults(
        cls,
        system_header: Optional[str] = None,
        context: Optional[str] = None,
    ) -> "CustomReActChatFormatter":
        """Create ReActChatFormatter from defaults."""
        if not system_header:
            system_header = (
                REACT_CHAT_SYSTEM_HEADER
                if not context
                else CONTEXT_REACT_CHAT_SYSTEM_HEADER
            )

        return CustomReActChatFormatter(
            system_header=system_header,
            context=context or "",
        )
        
def custom_failure_handler(callback_manager, exception):
    error_message = f"The agent encountered an error: {str(exception)}"
    return ToolOutput(content=error_message, tool_name="Error Handler")


react_system_prompt = PromptTemplate(REACT_CHAT_SYSTEM_HEADER_CUSTOM)

tools = [
    FunctionTool.from_defaults(
        fn=get_trending_pairs,
        name="get_trending_pairs", 
        description=(
            "Get trending trading pairs on the market."
            """Input args:
                jwt_token (str): User's authorization token
                resolution (str, optional): Time frame (default: "5m")
                limit (int, optional): Maximum number of pairs to return (default: 5)"""
            "Output: Price, market cap, liquidity, volume and performance metrics"
        ),
    ),
    FunctionTool.from_defaults(
        fn=search_token,
        name="search_token",
        description=(
            "Retrieves the token address based on the token name, symbol, or ticker."
            """Input args: 
                query (str): Token name, symbol, or ticker (e.g., 'SUDENG', 'hippo').
                jwt_token (str): User's authorization token"""
            "Output: Returns token information including:"
            "- Token address (contract address)"
            "- Token name"
            "- Token symbol"
            "- Token price"
            "- Liquidity (liquidityUsd)"
        ),
    ),
    FunctionTool.from_defaults(
        fn=scan_token,
        name="scan_token",
        description=(
            "Analyze token's trading metrics."
            """Input args:
                token_address (str): Token contract address"""
            "Output: Price, market cap, liquidity, volume and transaction counts"
        ),
    ),
]


def react_chat(
    query: str,
    llm=None,
    chat_history: List[ChatMessage] = None,
    max_iterations=10,
    jwt_token=None,
):
    formatter = CustomReActChatFormatter(jwt_token=jwt_token)
    agent = ReActAgent.from_tools(
        tools=tools,
        llm=llm,
        verbose=True,
        chat_history=chat_history,
        react_chat_formatter=formatter,
        max_iterations=max_iterations,
        output_parser=ReActOutputParser()
    )
    agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})
    response = agent.chat(query)
    
    
    # start task
    # task = agent.create_task(query)
    # print(f'task: {task}')
    # step_output = agent.run_step(task.task_id)
    # print(f'step_output.output: {step_output.output}')
    
    
    response = str(response)
    agent.reset()
    return response
