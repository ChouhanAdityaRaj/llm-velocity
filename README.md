<div align="center">
  <img src="data_collection\llm_velocity.png" alt="llm_velocity logo" />
</div>

# ⚡ Introduction

`llm_velocity` is a high-performance Python wrapper designed to optimize repeated Large Language Model (LLM) calls. It drastically reduces response times and token consumption through intelligent memory, all while providing native support for tool calling.

## ✨ Features

- **🚀 Smart Response Recall:** Never compute the same prompt twice. `llm_velocity` intelligently memorizes your previous requests, returning instant responses instead of making redundant API or local model calls.
- **📉 Token Efficient:** By eliminating duplicate requests and optimizing how context is passed, it drastically reduces your overall token usage and compute load.
- **🛠️ Native Tool Calling:** Seamlessly integrate external functions and APIs. `llm_velocity` fully supports tool calling (function calling), allowing your chosen LLM to interact with your Python code natively.
