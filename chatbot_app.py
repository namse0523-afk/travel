"""
OpenAI 기반 Streamlit 챗봇.

로컬: 프로젝트 루트에 `.env` 파일에 OPENAI_API_KEY 설정 후
      `streamlit run chatbot_app.py`

Streamlit Community Cloud 배포:
  1) GitHub에 이 저장소 연결
  2) New app → Main file: chatbot_app.py
  3) App settings → Secrets 에 아래 형식으로 입력:

     OPENAI_API_KEY = "sk-..."

  (로컬의 .streamlit/secrets.toml 은 커밋하지 말 것 — .gitignore 처리됨)
"""
from __future__ import annotations

import os
from typing import Any, Dict, Generator, List, Optional

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _openai_api_key() -> Optional[str]:
    key = (os.getenv("OPENAI_API_KEY") or "").strip()
    if key:
        return key
    try:
        v = st.secrets["OPENAI_API_KEY"]
        return (str(v).strip() if v else None) or None
    except Exception:
        return None


def _openai_client() -> Optional[OpenAI]:
    key = _openai_api_key()
    if not key:
        return None
    try:
        return OpenAI(api_key=key)
    except Exception:
        return None


def _build_messages(history: List[Dict[str, str]], system_prompt: str) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
    for m in history:
        role = m.get("role")
        content = (m.get("content") or "").strip()
        if role in ("user", "assistant") and content:
            out.append({"role": role, "content": content})
    return out


def _stream_assistant(
    client: OpenAI,
    messages: List[Dict[str, Any]],
    model: str,
    temperature: float,
) -> Generator[str, None, None]:
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        if delta:
            yield delta


def main() -> None:
    st.set_page_config(
        page_title="OpenAI 챗봇",
        page_icon="💬",
        layout="centered",
    )

    st.title("💬 OpenAI 챗봇")
    st.caption("Streamlit + OpenAI Chat Completions (스트리밍 응답)")

    if "cb_messages" not in st.session_state:
        st.session_state.cb_messages = []

    with st.sidebar:
        st.subheader("설정")
        model = st.selectbox(
            "모델",
            ["gpt-4o-mini", "gpt-4o"],
            index=0,
            help="비용·속도는 보통 gpt-4o-mini가 유리합니다.",
        )
        temperature = st.slider("temperature", 0.0, 2.0, 0.7, 0.05)
        system_prompt = st.text_area(
            "시스템 프롬프트",
            value=(
                "당신은 친절하고 정확한 도우미입니다. "
                "사용자가 한국어로 물으면 한국어로, 다른 언어로 물으면 그 언어에 맞춰 답합니다. "
                "모르는 것은 모른다고 하고, 추측과 사실을 구분합니다."
            ),
            height=120,
        )
        if st.button("대화 초기화", type="secondary"):
            st.session_state.cb_messages = []
            st.rerun()

        st.divider()
        st.markdown("**API 키**")
        key_ok = _openai_api_key() is not None
        if key_ok:
            st.success("OPENAI_API_KEY 감지됨")
        else:
            st.error(
                "키 없음. 로컬은 `.env`, 배포는 Streamlit Cloud **Secrets**에 "
                "`OPENAI_API_KEY` 를 설정하세요."
            )

    client = _openai_client()

    for msg in st.session_state.cb_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("메시지를 입력하세요…"):
        if not client:
            st.error("OpenAI 클라이언트를 만들 수 없습니다. API 키와 패키지 버전을 확인하세요.")
            return

        st.session_state.cb_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        api_messages = _build_messages(st.session_state.cb_messages, system_prompt)

        with st.chat_message("assistant"):
            try:
                acc: List[str] = []

                def gen() -> Generator[str, None, None]:
                    for t in _stream_assistant(
                        client, api_messages, model=model, temperature=temperature
                    ):
                        acc.append(t)
                        yield t

                st.write_stream(gen)
                assistant_text = "".join(acc)
            except Exception as e:
                assistant_text = f"(오류) {e}"
                st.error(assistant_text)

        st.session_state.cb_messages.append(
            {"role": "assistant", "content": assistant_text}
        )


if __name__ == "__main__":
    main()
