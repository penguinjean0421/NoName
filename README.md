# Slave
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue) ![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-red) ![Discord](https://img.shields.io/badge/discord-bot-5865F2?logo=discord&logoColor=white)

**Slave**는 서버 관리를 중심으로 실시간 로그 모니터링, 유틸리티 기능을 제공하는 다기능 디스코드 봇입니다. `config.json`을 통한 자동 서버 설정을 지원하며, `환경 변수(.env)`를 사용하여 보안성을 극대화했습니다.

---

## 🔗 상세 가이드
봇 설치 방법이나 상세 기능은 아래 문서를 참고해 주세요.
* [**🚀 시작하기 (setup.md)**](./docs/setup.md): 설치 및 환경 변수 설정
* [**⚙️ 서버 설정 가이드 (configuration.md)**](./docs/configuration.md): 로그 채널 설정 및 데이터 구조
* [**📜 명령어 요약 (commands.md)**](./docs/commands.md): 전체 명령어 및 기능 목록

## 초대하기
* **[ 🔗 Slave 초대하기 ](https://buly.kr/D3g9oYV)** 
    * ⚠️ 주의: 봇이 정상 작동하려면 서버 내에서 '관리자' 권한이 필요합니다.

## 📂 프로젝트 구조 (Project Structure)
```Plaintext
.
├── cogs/
│   ├── github.py                 # 깃허브 링크 및 검색 로직
│   ├── info.py                   # 도움말, 크레딧, 입장 알림
│   ├── system.py                 # 로그 시스템 및 관리 명령어
│   └── utility.py                # 기타 유틸리티 기능 (choose 등)
├── docs/
│   ├── commands.md               # 기능 명세 및 전체 명령어 목록
│   ├── configuration.md          # 서버별 독립 설정 및 JSON 데이터 구조 안내
│   ├── setup.md                  # 초기 설치, 환경 변수(.env) 설정 가이드
├── .env                          # [보안] 봇 토큰 및 환경 변수 설정 (GitHub 제외)
├── .env.example                  # 환경 변수 설정 샘플 파일
├── .gitignore                    # Git 추적 제외 목록 설정 파일
├── config.json                   # [자동생성] 서버별 상세 설정 데이터 (GitHub 제외)
├── config.example.json           # 서버 설정 데이터 샘플 파일
├── main.py                       # 봇 실행 메인 파일
├── README.md                     # 프로젝트 안내 및 사용법
└── requirements.txt              # 설치 필요한 라이브러리 목록
```

## 👤 Credits
* **Developer**: [penguinjean0421](https://github.com/penguinjean0421)
* Illustrator: aram
* Supporter: 목대 겜소과 친목 디코

## 📬 연락처 (Contact)
프로젝트에 대한 문의나 피드백은 아래 채널을 통해 연락주세요!

* **Email:** `penguinjean0421@gmail.com`
* **Discord:** `penguinjean0421`
* **GitHub:** [penguinjean0421](https://github.com/penguinjean0421)

## 📜 라이선스 (License)
* Copyright 2026. **penguinjean0421** All rights reserved.
    * 이 프로젝트의 코드와 리소스를 무단으로 복제, 수정, 배포하는 것을 금지합니다. 개인적인 학습 목적으로만 참고해 주시기 바랍니다.