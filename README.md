# Campus Mate — AI 학습 플래너

대학생이 과목, 시험까지 남은 기간, 하루 공부 가능 시간을 입력하면 AI가 학습 계획을 제안하는 반응형 웹 서비스입니다.

## 기술 스택
- 프론트엔드: HTML5, CSS3, Vanilla JavaScript
- 백엔드: Python, Vercel Serverless Functions (`api/plan.py`)
- AI: OpenAI API (`gpt-4o-mini`)
- 배포: GitHub + Vercel

## 페이지/섹션
1. 홈 — 서비스 소개
2. AI 플래너 — 입력 폼과 AI 학습 계획 출력
3. 학습 가이드 — 공부 팁 및 FAQ

## 실행 및 배포
1. GitHub에 전체 프로젝트를 업로드합니다.
2. Vercel에서 **Add New → Project**로 GitHub 저장소를 가져옵니다.
3. Framework Preset은 **Other**, Root Directory는 프로젝트 루트로 설정합니다.
4. Vercel 프로젝트의 **Settings → Environment Variables**에서 `OPENAI_API_KEY`를 등록합니다. 값은 OpenAI 플랫폼에서 발급한 실제 비밀 API 키입니다.
5. Production 환경에 적용하고 **Deploy** 또는 **Redeploy**합니다.
6. 배포된 URL에서 세 메뉴, 모바일 화면, AI 생성 및 오류 메시지를 확인합니다.

로컬 정적 화면 미리보기: 프로젝트 폴더에서 `python -m http.server 8000` 실행 후 `http://localhost:8000` 접속. **이 방식으로는 `/api/plan`이 실행되지 않습니다.** API까지 로컬 테스트하려면 Vercel CLI와 `vercel dev` 및 로컬 환경 변수 설정이 필요합니다.

## 환경 변수 및 보안
`OPENAI_API_KEY`는 Vercel 환경 변수에만 저장합니다. `.env` 파일, 코드, README, 스크린샷, GitHub 커밋에 실제 키를 넣지 않습니다. `.env.example`은 변수 이름만 보여주는 샘플입니다. 키가 노출되면 즉시 폐기하고 새로 발급하며 Git 이력에서도 노출을 제거해야 합니다. OpenAI API는 별도 과금 또는 사용량 제한이 적용될 수 있습니다.

## 요청 흐름
브라우저 폼 → JavaScript `fetch('/api/plan')` → Python 서버리스 함수 → OpenAI API → JSON 응답 → 화면 표시. 빈 입력, API 오류, 30초 타임아웃을 사용자에게 안내합니다.

## 배포 URL
(https://a1-3-sage.vercel.app/#home)

## 프로젝트 구조
```text
index.html
css/style.css
js/app.js
api/plan.py
requirements.txt
.env.example
.gitignore
README.md
SERVICE_PLAN.md
```
