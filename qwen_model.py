import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import psutil

token = "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"
# Initialize logging
logging.basicConfig(
    filename="chatbot_session.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Load the model and tokenizer
model_name = "Qwen/Qwen2.5-Coder-1.5b-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # Mixed precision for reduced memory
    device_map="auto"  # Automatically map to available GPUs or CPUs
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Function to log system stats
def log_system_stats():
    if torch.cuda.is_available():
        vram_allocated = torch.cuda.memory_allocated() / (1024 ** 2)
        vram_reserved = torch.cuda.memory_reserved() / (1024 ** 2)
        vram_total = torch.cuda.get_device_properties(0).total_memory / (1024 ** 2)
        logging.info(f"VRAM Usage: Allocated={vram_allocated:.2f}MB, Reserved={vram_reserved:.2f}MB, Total={vram_total:.2f}MB")
    else:
        logging.info("No GPU available. Running on CPU.")

    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    logging.info(f"CPU Usage: {cpu_usage}% | RAM Usage: {ram_usage}%")

# Chatbot session class
class ChatBotSession:
    def __init__(self, model, tokenizer, max_context_tokens=2000):
        self.model = model
        self.tokenizer = tokenizer
        self.chat_history = [
            {"role": "system", "content": "Вы являетесь помощником гейммастера. Строго следуйте инструкциям и делайте то, что в них указано."}
        ]
        self.max_context_tokens = max_context_tokens

    def _truncate_history(self):
        while True:
            text = self.tokenizer.apply_chat_template(
                self.chat_history,
                tokenize=False,
                add_generation_prompt=False
            )
            tokenized = self.tokenizer(text, return_tensors="pt")
            token_count = tokenized.input_ids.size(1)

            logging.info(f"Current token count: {token_count}. Max allowed: {self.max_context_tokens}.")
            if token_count <= self.max_context_tokens:
                break

            if len(self.chat_history) > 2:
                removed_user = self.chat_history[1]["content"]
                removed_assistant = self.chat_history[2]["content"]
                self.chat_history.pop(1)
                self.chat_history.pop(1)

                logging.info(f"Truncated history. Removed oldest messages:\nUser: {removed_user}\nAssistant: {removed_assistant}")
            else:
                break

    def process_task(self, task, scenario, question, max_new_tokens=512):
        if question:
            self.chat_history.append({"role": "user", "content": question})
            self._truncate_history()

            prompt = f"Задание: {task}\nСценарий: {scenario}\nВопрос: {question}\nДайте полезную подсказку, но нигода не давай ответа, только подсказки"
            print(prompt)
            self.chat_history.append({"role": "user", "content": prompt})

            text = self.tokenizer.apply_chat_template(
                self.chat_history,
                tokenize=False,
                add_generation_prompt=True
            )
            model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

            # Log system stats before inference
            log_system_stats()

            torch.cuda.empty_cache()  # Clear GPU memory before inference
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=max_new_tokens
            )
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]
            response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

            self.chat_history.append({"role": "assistant", "content": response})

            # Log system stats after inference
            log_system_stats()
        else:
            response = None

        return response

    def check_code(self, code, max_new_tokens=512):
        prompt = f"Is the following code correct?\n{code}\nAnswer with 'True' or 'False'."
        text = self.tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        # Log system stats before inference
        log_system_stats()

        torch.cuda.empty_cache()  # Clear GPU memory before inference
        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # Log system stats after inference
        log_system_stats()
        # Return response (True or False)
        if "True" in response:
            return True
        elif "False" in response:
            return False
        else:
            return None  # In case the model gives an unexpected response

    def __enter__(self):
        logging.info("Chatbot session started.")
        print("Chatbot session started.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info("Chatbot session ended.")
        print("Chatbot session ended.")

# Example use of the ChatBotSession class in the main script
def task_helper(task, scenario, question):
    with ChatBotSession(model, tokenizer, max_context_tokens=2000) as chat_session:

       
        #code = ""  
    
        # Example interaction
        # task = "Математическая задача"
        # scenario = "Веди себя как эльф, отвейчай на вопросы."
        # question = "Сколько будет 2+2?"

        # Use the process_task function to generate a response
        response = chat_session.process_task(task, scenario, question)
        print(response)
        return response
    
def task_verify(code):
    with ChatBotSession(model, tokenizer, max_context_tokens=2000) as chat_session:
        
        # Example code check interaction
        # code = "def add(a, b):\n    return a + b"
        is_code_correct = chat_session.check_code(code)
        print( is_code_correct)
# task = "Математическая задача"
# scenario = "Веди себя как эльф, отвейчай на вопросы."
# question = "Сколько будет 2+2?"
# task_helper(task, scenario, question)





 
