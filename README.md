# LLM with One Tool Integration
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/Abhaykumarbadam/llm-with-one-tool-integration)

This repository demonstrates a simple chatbot that integrates a Large Language Model (Groq's Llama 3) with a local calculator tool. The application intelligently analyzes user input to decide whether to handle the query with the LLM for general knowledge or route it to the calculator for mathematical computations.

## Features

- **LLM Integration**: Utilizes the Groq API for fast LLM inference with the Llama 3 8B model.
- **Tool Integration**: Seamlessly uses a local calculator tool for evaluating mathematical expressions.
- **Intelligent Routing**: Employs regular expressions and NLTK for part-of-speech tagging to determine the nature of the user's query.
- **Specific Handlers**: Includes dedicated logic for simple greetings, math questions, general knowledge questions, and multi-part queries.
- **Interaction Logging**: All conversations are timestamped and saved to `interaction_logs.json` for review.

## How It Works

The chatbot processes user input through a series of checks to determine the appropriate action:

1.  **Greeting Check**: If the input is a simple greeting (e.g., "hi", "hello"), the bot provides a standard greeting without calling the LLM.
2.  **Multi-Query Check**: The bot checks if the input contains both a math question and a general knowledge question (e.g., "What is 5+5 and the capital of France?"). If so, it asks the user to pose one question at a time.
3.  **Math Expression Check**: If the input contains a mathematical operation, it's passed to the `calculator_tool` for evaluation. The tool can handle both direct expressions (`12 * 7`) and natural language queries (`Add 45 and 30`).
4.  **General Question Check**: If the input is identified as a general question (e.g., "What is the capital of France?"), it is sent to the Groq LLM for a concise answer.
5.  **Default LLM Fallback**: For any other type of query, the input is sent to the Groq LLM with a prompt that encourages a step-by-step explanation.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/abhaykumarbadam/llm-with-one-tool-integration.git
    cd llm-with-one-tool-integration
    ```

2.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    Alternatively, you can install them manually:
    ```bash
    pip install requests python-dotenv nltk
    ```

3.  **Set up your API Key:**
    Create a file named `.env` in the root directory of the project and add your Groq API key:
    ```
    GROQ_API_KEY='your_groq_api_key_here'
    ```

4.  **Download NLTK resources:**
    The first time you run the application, you need to download the necessary NLTK data packages. Uncomment the following lines at the top of `chatbot_with_tool.py`, run the script once, and then you can comment them out again.
    ```python
    # import nltk
    # nltk.download("punkt")
    # nltk.download("averaged_perceptron_tagger")
    ```

## Usage

To start the chatbot, run the `chatbot_with_tool.py` script from your terminal:

```bash
python chatbot_with_tool.py
```

The application will prompt you for input. Type `exit` to end the session and save the conversation log.

### Example Interactions

**Greeting:**
```
You: hi
Bot: Hello! How can I help you today?
```

**Calculation:**
```
You: What is 12 times 7?
Bot: The calculator tool is being used.
The result is: 84.0
```

**General Question:**
```
You: what is the capital of france?
Bot: The capital of France is Paris.
```

**Multi-Query:**
```
You: Multiply 9 and 8, and also tell me the capital of Japan.
Bot: I'm currently not able to handle multiple questions in a single input. Please ask one at a time.
```

## File Descriptions

-   `chatbot_with_tool.py`: The main application file containing the chatbot logic, query routing, and API calls.
-   `calculator_tool.py`: A simple module that provides the `calculate` function to evaluate mathematical expressions.
-   `interaction_logs.json`: A log file where conversation history is stored in JSON format.