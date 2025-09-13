# server.py
from mcp.server.fastmcp import FastMCP
import sys
import logging
import os
from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageType

logger = logging.getLogger('CozeBot')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

import math
import random

# Create an MCP server
mcp = FastMCP("CozeBot")

# Request Coze Bot
@mcp.tool()
def coze_knowledge_request(question: str) -> dict:
    """
    Request coze knowledge base for information.

    Args:
        question (str): The prompt to ask the coze agent with knowledge base agent.

    Returns:
        dict: The response from the coze knowledge base.
    """
    bearer = os.environ.get('COZE_BEARER')
    if not bearer:
        logger.error("Please set the `COZE_BEARER` environment variable")
        sys.exit(1)
    coze = Coze(auth=TokenAuth(token=bearer), base_url="https://api.coze.cn")
    chat_poll = coze.chat.create_and_poll(
        bot_id="7549025197796081674",
        user_id="bot666",
        additional_messages=[
            Message.build_user_question_text(question),
        ],
    )
    result = ""
    for message in chat_poll.messages:
        # print(message.content, end="", flush=True)
        if message.role == "assistant" and message.type == MessageType.ANSWER:
            result += message.content

    if chat_poll.chat.status == ChatStatus.COMPLETED:
        print()
        print("token usage:", chat_poll.chat.usage.token_count)
    return {"success": True, "result": result}

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
    # coze_knowledge_request("What is the capital of France?")
