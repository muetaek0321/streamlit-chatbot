import os
model_dir = "./pretrained"
if not os.path.isdir(model_dir):
    os.makedirs(model_dir, exist_ok=True)
os.environ["HF_HOME"] = model_dir

from transformers import AutoProcessor, Gemma3ForConditionalGeneration
import torch
# from huggingface_hub import login
# login()

model_id = "google/gemma-3-4b-it"

model = Gemma3ForConditionalGeneration.from_pretrained(
    model_id, device_map="auto"
).eval()

processor = AutoProcessor.from_pretrained(model_id)

# messages = [
#     {
#         "role": "system",
#         "content": [{"type": "text", "text": "あなたは日本語で回答するアシスタントです。"}]
#     },
#     {
#         "role": "user",
#         "content": [
#             {"type": "image", "image": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg"},
#             {"type": "text", "text": "画像の内容を教えてください。"}
#         ]
#     }
# ]
messages = [
    {
        "role": "system",
        "content": [{"type": "text", "text": "あなたは日本語で回答するアシスタントです。"}]
    },
    {
        "role": "user",
        "content": [{"type": "text", "text": "エレファントカシマシについて教えてください。"}]
    }
]

inputs = processor.apply_chat_template(
    messages, add_generation_prompt=True, tokenize=True,
    return_dict=True, return_tensors="pt"
).to(model.device, dtype=torch.bfloat16)

input_len = inputs["input_ids"].shape[-1]

with torch.inference_mode():
    generation = model.generate(**inputs, max_new_tokens=1000, do_sample=False)
    generation = generation[0][input_len:]

decoded = processor.decode(generation, skip_special_tokens=True)
print(decoded)
