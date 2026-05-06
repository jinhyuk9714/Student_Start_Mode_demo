# Hana EZ Student Start Mode 데모

![Student Start Mode 데모 미리보기](output/video/demo_88s_euna_preview.gif)

외국인 유학생의 입국 초기 금융 온보딩을 `Hana EZ` 안의 맞춤 체크리스트 흐름으로 보여주는 발표용 정적 HTML 데모입니다. **하나 청년 금융인재 양성 프로젝트**에서 디지털기술(AI, 블록체인 등)을 활용한 ESG 및 미래금융서비스 개발 주제로 진행한 4인 프로젝트 산출물입니다. 최종 시연 기준 파일은 `demo.html`이며, 동일한 최종본을 보관하기 위해 `demo_88s_euna.html`도 함께 유지합니다.

## 프로젝트 맥락

이 저장소는 단순 정적 페이지 실험이 아니라, 하나 청년 금융인재 양성 프로젝트 안에서 유학생 금융 접근성 문제를 미래금융서비스 관점으로 풀어낸 발표용 프로토타입입니다. README에서는 최종 데모 파일뿐 아니라, 금융 온보딩 문제 정의와 Hana EZ 기반 시연 흐름이 드러나도록 정리합니다.

| 구분 | 내용 |
| --- | --- |
| 진행 프로젝트 | 하나 청년 금융인재 양성 프로젝트 |
| 주제 | 디지털기술(AI, 블록체인 등)을 활용한 ESG 및 미래금융서비스 개발 |
| 팀 규모 | 4인 프로젝트 |
| 산출물 | 유학생 금융 온보딩을 시연하는 Hana EZ Student Start Mode 정적 HTML 데모 |

## 문제와 아이디어

유학생은 입국 직후 비자, ARC, 휴대폰, 계좌, 카드, 송금처럼 서로 의존하는 절차를 짧은 시간 안에 처리해야 합니다. 이 데모는 사용자의 학교, 비자, 국적, ARC 상태, 필요한 금융 서비스를 입력받아 지금 가능한 일과 다음에 해야 할 일을 구분해 보여주는 온보딩 경험을 시각화합니다.

핵심 방향은 "정보를 모아두는 화면"보다 "현재 상태에서 필요한 금융 여정을 먼저 정리해 주는 화면"입니다. 체크리스트 판단은 상태와 규칙을 중심으로 두고, AI 채팅은 사용자의 세부 질문과 상황 설명을 돕는 보조 역할로 설계했습니다.

## 주요 시나리오

- 온보딩 설문: 학교, 비자, 국적, ARC 수령 상태, 필요한 금융 서비스 선택
- 금융 체크리스트: 지금 가능, 다음 단계, 잠김 항목을 나눠 표시
- 상태 변화 반영: ARC 수령 같은 변화가 생기면 잠긴 항목을 해제하고 다음 작업을 안내
- 스마트 캘린더: 비자 만료일, ARC 수령일, 계좌 개설 권장일, 건강검진, 체크카드 발급 일정 표시
- AI 금융 도우미: 이체 한도, 장학금 계좌, 서류 준비처럼 맥락형 질문에 답변
- 출처 표시: 하나은행과 금융 규정 기반 안내임을 UI 안에서 함께 노출

## 최종 산출물

| 구분 | 파일 | 설명 |
| --- | --- | --- |
| 최종 HTML | [demo.html](demo.html) | 발표와 녹화에 사용하는 기본 진입 파일 |
| 보관용 HTML | [demo_88s_euna.html](demo_88s_euna.html) | 최종본 원본 이름을 유지한 동일 HTML |
| 최종 MP4 | [output/video/demo_88s_euna_final.mp4](output/video/demo_88s_euna_final.mp4) | 4K H.264 + AAC 발표 영상 |
| README GIF | [output/video/demo_88s_euna_preview.gif](output/video/demo_88s_euna_preview.gif) | 전체 흐름을 빠르게 훑는 미리보기 |
| 오디오 이벤트 | [docs/audio/demo_88s_euna_audio_events.md](docs/audio/demo_88s_euna_audio_events.md) | 효과음 타임코드와 역할 |
| 오디오 소스 | [docs/audio/demo_88s_euna_audio_sources.md](docs/audio/demo_88s_euna_audio_sources.md) | 배경음악과 효과음 출처 |

## 실행 방법

정적 HTML 데모라 별도 빌드가 필요하지 않습니다. 이미지와 폰트 로딩을 안정적으로 확인하려면 로컬 서버로 여는 편이 좋습니다.

```bash
python3 -m http.server 8000
```

브라우저에서 아래 주소를 엽니다.

```text
http://localhost:8000/demo.html?mode=short
```

`mode=short`는 짧은 발표 흐름 확인에 사용합니다. 전체 타임라인을 확인하려면 쿼리 없이 `demo.html`을 열면 됩니다.

## 파일 구조

```text
.
├─ demo.html
├─ demo_88s_euna.html
├─ imgs/
│  ├─ greet.png
│  └─ star.png
├─ docs/audio/
│  ├─ demo_88s_euna_audio_events.md
│  └─ demo_88s_euna_audio_sources.md
├─ output/
│  ├─ audio_work/
│  └─ video/
├─ user_documents/           # 아이디어, 배경, 아키텍처, 발표 자료 초안
└─ archive/html/             # 이전 실험 HTML 보관
```

## 구현 포인트

- 하나의 HTML 안에서 모바일 앱 형태의 온보딩, 체크리스트, 캘린더, 채팅 화면을 순차 시연
- `mode` 파라미터로 발표 길이에 맞춘 pacing 조정
- 영상 제작을 위해 타이틀 카드, 푸시 배너, 탭 전환, 채팅 입력, 출처 표시 타이밍을 스크립트화
- 배경음악과 UI 효과음의 출처 및 사용 타임코드를 문서로 분리

## 참고 사항

- 실제 금융 상품 가입이나 외부 서비스 호출을 수행하지 않는 발표용 프로토타입입니다.
- `user_documents/`에는 공모전 배경, 아이디어 제안, 경쟁사 분석, 상태 전이 설계 등 기획 산출물이 함께 들어 있습니다.
- 기존 실험 HTML은 `archive/html/`에 보관하고, 발표 기준은 루트의 `demo.html`로 통일했습니다.
