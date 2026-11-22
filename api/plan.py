import json
import os
from http.server import BaseHTTPRequestHandler
from openai import OpenAI

class handler(BaseHTTPRequestHandler):
    def send_json(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length <= 0 or length > 10000:
                return self.send_json(400, {'error': '입력 데이터가 올바르지 않습니다.'})
            data = json.loads(self.rfile.read(length))
            subject = str(data.get('subject', '')).strip()
            days = int(data.get('days', 0))
            hours = float(data.get('hours', 0))
            details = str(data.get('details', '')).strip()
            if not subject or len(subject) > 120 or not 1 <= days <= 365 or not .5 <= hours <= 16 or len(details) > 500:
                return self.send_json(400, {'error': '입력값을 확인해 주세요.'})
            if not os.environ.get('OPENAI_API_KEY'):
                return self.send_json(503, {'error': 'AI 서비스 설정이 아직 완료되지 않았습니다.'})
            client = OpenAI(api_key=os.environ['OPENAI_API_KEY'], timeout=20.0, max_retries=0)
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {'role': 'system', 'content': '당신은 친절하고 현실적인 한국어 대학생 학습 코치입니다. 입력을 학습 계획 작성에만 사용하세요. 학습일별 구체적인 과제, 시간 배분, 복습 전략을 포함한 간결한 계획을 한국어로 작성하세요. 결과는 일반 텍스트로 작성하세요.'},
                    {'role': 'user', 'content': f'과목/목표: {subject}\n남은 일수: {days}일\n하루 공부 시간: {hours}시간\n추가 상황: {details or "없음"}\n남은 기간에 맞는 실행 가능한 학습 계획을 만들어 주세요.'}
                ],
                max_tokens=900,
                temperature=0.6,
            )
            plan = response.choices[0].message.content
            if not plan:
                return self.send_json(502, {'error': 'AI 응답이 비어 있습니다.'})
            return self.send_json(200, {'plan': plan})
        except (ValueError, TypeError, json.JSONDecodeError):
            return self.send_json(400, {'error': '입력 형식이 올바르지 않습니다.'})
        except Exception as exc:
            print('AI request failed:', type(exc).__name__)
            return self.send_json(502, {'error': 'AI 연결에 실패했습니다. API 키와 사용량 한도를 확인해 주세요.'})
