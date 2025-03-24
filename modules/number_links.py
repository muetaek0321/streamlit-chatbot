
import streamlit as st


DATA_PATH = "./data/elekashi_numbers.csv"

def load_urls() -> dict:
    numbers = dict()
    with open(DATA_PATH, mode="r", encoding="cp932") as f:
        for number_info in f.read().split("\n"):
            if "," in number_info:
                number, url = number_info.split(",")
                numbers[number] = url
            
    return numbers


def response_add_info(
    response_text: str
) -> str:
    """アシスタントの返答にある曲目を見つけてその曲のリンクを追加する
    """
    if "numbers" not in st.session_state:
        st.session_state.numbers = load_urls()
    
    add_info = []
    for number, url in st.session_state.numbers.items():
        if number in response_text:
            add_info.append(f"<b>{number}</b>:<br><a href={url}>{url}</a>")
            
    if len(add_info) == 0:
        return ""
    else:
        return "<hr><span style=\"font-size : 10pt\">"+"<br><br>".join(add_info)+"</span><hr>"

