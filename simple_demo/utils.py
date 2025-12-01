import subprocess
import time
import os


os.environ['OLLAMA_HOST'] = '127.0.0.1:11438'


def start_ollama_server():
    # Start the Ollama server in a subprocess
    ollama_process = subprocess.Popen(['ollama', 'serve'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the server to start
    print("Starting Ollama server...")
    time.sleep(1)  # Wait for the server to initialize

    print("Ollama server is running on 127.0.0.1:11438")

def stop_ollama_server(ollama_process):
    # Terminate the Ollama server subprocess
    ollama_process.terminate()
    ollama_process.wait()
    print("Ollama server has been stopped.")

def pull_model(model_name):
    # Pull a model (e.g., llama)
    model = model_name
    print("Pulling the llama model...")
    subprocess.run(['ollama', 'pull', model])