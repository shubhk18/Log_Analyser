# Log_Analyser

## Architecture

The application consists of two main components:

*   `mcp_server.py`: A Python script that creates an HTTP server to serve log files. It has a predefined list of accessible log files.
*   `start_chat.sh`: A shell script that uses OLLAMA to create a temporary chat model with the contents of a log file as context. This allows you to chat with your log files.
*   **Log files**: Plain text files containing log data (`mysql_connection_detailed.log`, `detailed_log.txt`, etc.).

## How to run the project

1.  **Start the server**: In one terminal, run the Python server:
    ```bash
    python3 mcp_server.py
    ```
2.  **Start the chat session**: In another terminal, run the `start_chat.sh` script. You can optionally specify the OLLAMA model and the log file to use.
    ```bash
    # Start a chat with the default model and log file
    ./start_chat.sh

    # Specify a model
    ./start_chat.sh mistral

    # Specify a model and a log file
    ./start_chat.sh llama3 mysql_connection_detailed.log
    ```

## Data Flow

1.  The user runs the `mcp_server.py` script, which starts an HTTP server.
2.  The user runs the `start_chat.sh` script.
3.  The script fetches the specified log file from the running Python server using `curl`.
4.  A temporary OLLAMA model is created with the log file's content embedded in its system prompt.
5.  An interactive chat session is started with the temporary model.
6.  The user can now ask questions about the log file in the chat.
7.  When the chat is closed, the temporary model and its files are automatically cleaned up.
