# 🤖 Slave
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue) ![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-red) ![Discord](https://img.shields.io/badge/discord-bot-5865F2?logo=discord&logoColor=white)

**Slave**는 서버 관리를 최적화하고 사용자 편의를 돕기 위해 설계된 다기능 디스코드 봇입니다. [DSMB 템플릿](https://github.com/penguinjean0421/DSMB)을 기반으로 제작된 표준 모델로, 강력한 로그 시스템과 스마트한 관리 기능을 제공합니다.

---

## 🔗 시작하기
* **[🔗 Slave 초대하기](https://buly.kr/D3g9oYV)**
* **[📜 전체 명령어 목록 확인](./docs/commands.md)**
* ⚠️ **주의**: 봇의 모든 관리 기능(로그, 뮤트, 차단 등)이 정상 작동하려면 서버 내에서 **'관리자(Administrator)'** 권한이 반드시 필요합니다.

---

## ✨ 핵심 기능 (Core Features)

### 🛡️ 서버 관리 및 보안 (Moderation)
* **스마트 제재**: 타임아웃, 추방, 차단 기능을 지원하며 `10m`, `1h`, `1d`와 같은 직관적인 시간 단위를 인식합니다.
* **음성 채널 제어**: 유저를 강제로 퇴장시키거나(vckick), 개별 뮤트/데픈 설정을 관리할 수 있습니다.

### 📝 실시간 로그 시스템 (Logging)
* **메시지 추적**: 메시지 삭제 및 수정 내역을 실시간으로 기록하여 서버 내 분쟁을 방지합니다.
* **음성 활동 로그**: 멤버의 채널 입장, 퇴장 및 이동 경로를 상세히 기록합니다.
* **처벌 전용 채널**: 관리 내역(뮤트, 차단 등)만 별도로 모으는 `punish` 로그를 지원합니다.

### 🎲 유틸리티 & 편의 기능 (Utility)
* **메뉴 추천**: 아침/점심/저녁 상황에 맞는 메뉴를 무작위로 추천합니다.
* **결정 도우미**: 선택하기 어려운 고민거리를 `choose` 명령어로 해결해 드립니다.
* **GitHub 연동**: 프로젝트 링크나 프로필을 빠르게 공유할 수 있습니다.

---

## ⚙️ 빠른 설정 가이드 (Admin Only)
봇 초대 후, 관리자 권한을 가진 유저가 아래 명령어를 입력하여 로그 채널을 설정해 주세요.

1. `!set log [#채널]`: 일반 활동 로그(메시지 수정/삭제 등) 채널 지정
2. `!set punish [#채널]`: 제재 내역(뮤트/차단 등) 전용 채널 지정
3. `!set bot [#채널]`: 봇 명령어 사용을 허용할 전용 채널 지정

---

## 📂 프로젝트 정보
본 봇은 개발자용 템플릿인 **DSMB**를 기반으로 구현되었습니다. 봇의 내부 구조나 직접 구동 방식이 궁금하시다면 아래 문서를 참고하세요.
* [**🛠️ DSMB 템플릿 구조 보기**](./README.md)
* [**🚀 직접 호스팅하기 (setup.md)**](./docs/setup.md)

---

## 👤 Credits & Contact
* **Developer**: [penguinjean0421](https://github.com/penguinjean0421)
* **Illustrator**: aram
* **Supporter**: 목대 겜소과 친목 디코
* **Contact**: [Email](mailto:penguinjean0421@gmail.com) | [Discord](https://discord.com/users/penguinjean0421)

## 📜 라이선스 (License)
* Copyright 2026. **penguinjean0421** All rights reserved.
    * 이 프로젝트의 코드와 리소스를 무단으로 복제, 수정, 배포하는 것을 금지합니다. 개인적인 학습 및 템플릿 활용 목적으로만 참고해 주시기 바랍니다.

## 📖 가이드 및 문서
* [**📜 명령어 요약 (commands.md)**](./docs/commands.md) : "봇 사용법이 궁금해요."
* [**⚙️ 서버 설정 가이드 (configuration.md)**](./docs/configuration.md) : "로그 채널을 설정하고 싶어요."
* [**🚀 직접 호스팅하기 (setup.md)**](./docs/setup.md) : "코드를 내려받아 직접 구동하고 싶어요."

> 💡 **개발자이신가요?** 이 봇의 기반이 된 **DSMB 템플릿**의 구조와 확장 방법은 [DSMB 저장소](https://github.com/penguinjean0421/DSMB)에서 확인하실 수 있습니다.