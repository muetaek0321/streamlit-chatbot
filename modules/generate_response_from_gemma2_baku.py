import os
model_dir = "./pretrained"
if not os.path.isdir(model_dir):
    os.makedirs(model_dir, exist_ok=True)
os.environ["HF_HOME"] = model_dir
import time
import traceback

import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
from markdown import Markdown


# AIの返答を作成
def gemma2_baku_generator():    
    # 返答を作成
    # try:
    model_id = "rinna/gemma-2-baku-2b-it"
    dtype = torch.bfloat16

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="cuda",
        torch_dtype=dtype,
        attn_implementation="eager",
    )
    
    user_input = [st.session_state.messages[-1]]
    
    prompt = tokenizer.apply_chat_template(user_input, tokenize=False, add_generation_prompt=True)

    input_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt").to(model.device)
    outputs = model.generate(
        input_ids,
        max_new_tokens=512,
    )

    response = tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True)
    
    # 返答を成形（makrddown -> HTML）
    response = Markdown().convert(response)
    # except Exception:
    #     # API側のエラーをキャッチして表示する
    #     response = f"<span style=\"color:#ff0000;\">{traceback.format_exc()}</span>"
    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)