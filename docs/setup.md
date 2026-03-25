# 🚀 시작하기 (Getting Started)
**Slave** 봇을 로컬 환경이나 서버에서 구동하기 위한 가이드입니다. 이 문서는 봇의 설치부터 실행, 초기 환경 설정까지의 과정을 다룹니다.

---

## 1. 요구 사항 (Requirements)
* **Python 3.8 이상**: 최신 `discord.py` 라이브러리와의 호환성을 위해 필요합니다.
* **Discord Bot Token**: [Discord Developer Portal](https://discord.com/developers/applications)에서 애플리케이션 생성 후 발급받은 토큰이 필요합니다.
* **Intents 설정**: 봇 설정(Bot 탭)에서 `Privileged Gateway Intents` 항목의 모든 옵션을 활성화해야 정상 작동합니다.

## 2. 설치 및 실행 (Installation)
터미널 또는 커맨드 라인에서 아래 명령어를 순차적으로 입력하세요.

```bash
# 1. 저장소 복제
git clone https://github.com/penguinjean0421/Slave.git
cd Slave

# 2. 필수 라이브러리 설치
pip install -r requirements.txt

# 3. 봇 실행
python main.py
```

## 3. 환경 변수 설정 (`.env`)
보안을 위해 봇 토큰은 코드 내에 직접 입력하지 않습니다. 프로젝트 루트에 `.env` 파일을 생성하고 아래 형식을 참고하여 입력하세요.

> Tip: `.env.example` 파일을 복사하여 `.env`로 이름을 변경한 뒤 수정하면 편리합니다.

```Ini, TOML
# Discord Token (절대 공유 금지)
BOT_TOKEN=your_token_here_do_not_share

# Prefixes (여러 개 설정 시 콤마(,)로 구분)
BOT_PREFIXES=!

# API 
# WEATHER_API_KEY=your_api_key_here
```

## ⚠️ 중요 보안 및 운영 팁
* **🚨 보안 주의**: `.env`와 `config.json`은 민감한 정보가 포함되어 있으므로 절대 GitHub에 업로드하지 마세요.
    * 본 프로젝트는 `.gitignore`를 통해 해당 파일들을 추적 대상에서 제외하고 있습니다.
* **👑 권한 설정**: 봇이 로그 추적 및 멤버 관리 기능을 정상적으로 수행하려면 서버 내에서 반드시 **'관리자(Administrator)'** 권한이 필요합니다.
* **🛠️ 설정 확인**: 봇이 실행된 후, 관리자 계정으로 서버 설정 명령어(`!set`)를 사용하여 로그 채널을 지정해 주세요.

## 🔗 관련 문서
* [**🏠 메인 페이지로 돌아가기 (README.md)**](../README.md)
* [**⚙️ 서버 설정 가이드 (configuration.md)**](./configuration.md)
    * 서버별 로그 채널 설정 방법 및 `config.json` 데이터 구조 안내
* [**📜 명령어 요약 (commands.md)**](./commands.md)
    * 관리자 및 일반 유저가 사용할 수 있는 전체 명령어 목록