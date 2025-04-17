import os
model_dir = "./pretrained"
if not os.path.isdir(model_dir):
    os.makedirs(model_dir, exist_ok=True)
os.environ["HF_HOME"] = model_dir
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "rinna/gemma-2-baku-2b-it"
dtype = torch.bfloat16

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="cuda",
    torch_dtype=dtype,
    attn_implementation="eager",
)

chat = [
    { "role": "user", "content": "エレファントカシマシについて教えてください。" },
]
prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

input_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt").to(model.device)
outputs = model.generate(
    input_ids,
    max_new_tokens=512,
)

response = tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True)
print(response)