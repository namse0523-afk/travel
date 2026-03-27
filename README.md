# 여행 계획 & OpenAI 챗봇 (Streamlit)

이 저장소에는 **여행 플래너**(`app.py`)와 **챗봇**(`chatbot_app.py`)이 있습니다.  
Streamlit Community Cloud에서는 **앱마다 진입 파일(Main file)** 을 한 개만 지정할 수 있으므로, 같은 레포로 **앱을 두 번 등록**하면 됩니다.

## GitHub에 올리기

```bash
git status
git add -A
git commit -m "Describe your change"
git push origin master
```

- `.env`는 `.gitignore`에 있어 커밋되지 **않습니다**. API 키는 GitHub에 넣지 마세요.
- 원격이 없다면 GitHub에서 새 레포를 만든 뒤:

  ```bash
  git remote add origin https://github.com/<사용자>/<레포>.git
  git branch -M main   # 또는 master 유지
  git push -u origin main
  ```

## Streamlit Community Cloud 배포

1. [share.streamlit.io](https://share.streamlit.io) 에 로그인 → **GitHub 연동**.
2. **New app** → 이 저장소 선택.
3. **Main file path**:
   - 여행 플래너: `app.py`
   - 챗봇만 쓸 때: `chatbot_app.py`
4. **Advanced settings**에서 Python 버전은 기본값이면 보통 무난합니다. 문제가 있으면 저장소 루트의 `runtime.txt`를 참고하세요.
5. 앱 **Settings → Secrets**에 다음을 붙여 넣습니다 (`secrets.toml.example` 참고):

   ```toml
   OPENAI_API_KEY = "sk-proj-여기에_본인_키"
   ```

6. **Save** 후 재배포(Redeploy).

로컬에서만 쓰는 비밀값은 `.streamlit/secrets.toml`에 두되, 이 파일은 **절대 커밋하지 마세요**.

## 로컬 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

챗봇만:

```bash
streamlit run chatbot_app.py
```

Windows에서는 `run_app.bat`, `run_chatbot.bat`을 사용할 수 있습니다.

## 레포 구성 요약

| 경로 | 설명 |
|------|------|
| `app.py` | 여행 계획 메인 앱 |
| `chatbot_app.py` | OpenAI 챗봇 |
| `requirements.txt` | Cloud가 설치하는 패키지 |
| `runtime.txt` | (선택) Cloud Python 버전 |
| `.streamlit/config.toml` | Streamlit 동작 옵션 |
| `.streamlit/secrets.toml.example` | Secrets 입력 예시 (비밀 아님) |
