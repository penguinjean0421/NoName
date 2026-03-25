# ⚙️ 서버 설정 및 구조 (Server Configuration)

Slave는 각 서버의 독립적인 운영을 위해 `config.json` 파일을 사용하여 설정을 관리합니다. 이 문서는 서버별 설정 방법과 내부 데이터 구조에 대해 설명합니다.

---

## 1. 채널 설정 명령어 (Admin Only)
봇이 서버에 처음 입장하면 모든 채널 설정값은 `None`으로 초기화됩니다. 서버 관리자 권한을 가진 유저가 아래 명령어를 입력하여 각 기능을 활성화해야 합니다.

* `!set log [#채널]` : 메시지 수정/삭제 등 일반 활동 로그 채널 지정
* `!set punish [#채널]` : 뮤트, 타임아웃, 차단 등 제재 내역 로그 채널 지정
* `!set bot [#채널]` : 봇 명령어 사용이 허용되는 전용 채널 지정

## 2. `config.json` 상세 데이터 구조
봇은 서버 고유 ID(Guild ID)를 키로 하여 데이터를 관리합니다.

| 필드명 (Key) | 초기값 (Default) | 설명 | 업데이트 방법 |
| :---: | :---: | :---: | :---: |
| `server_name` | `guild.name` | 서버의 현재 이름 | 자동 갱신 |
| `owner_id` | `guild.owner_id` | 서버 소유자의 고유 ID | 자동 관리 |
| `owner_name` | `str(guild.owner)` | 서버 소유자의 이름 및 태그 | 자동 갱신 |
| `log_channel_id` | `None` | 일반 활동 로그 채널 ID | `!set log` 명령어 |
| `punish_log_channel_id` | `None` | 제재(처벌) 내역 로그 채널 ID | `!set punish` 명령어 |
| `command_channel_id` | `None` | 봇 명령어 전용 채널 ID | `!set bot` 명령어 |

### 📄 데이터 예시 (config.json)
```json
{
  "123456789012345678": {
    "server_name": "테스트 서버",
    "owner_id": 987654321098765432,
    "owner_name": "User#0000",
    "log_channel_id": 111222333444555,
    "punish_log_channel_id": null,
    "command_channel_id": 555444333222111
  }
}
```

## 3. 데이터 관리 특징
* **자동 생성 및 갱신**: 봇이 서버 정보를 감지하여 기본 틀을 생성하며, 서버 이름이나 소유자 변경 시 실시간으로 데이터를 동기화합니다.
* **영속성 유지**: 설정된 값은 즉시 파일에 저장(`save_config`)되어 봇이 재시작되어도 설정이 유지됩니다.
* **⚠️ 보안 주의**: `config.json`에는 서버 고유 ID와 상세 채널 정보가 담겨 있습니다. 보안을 위해 절대 외부에 공유하거나 GitHub에 업로드하지 마세요.
    * 본 프로젝트는 `.gitignore`를 통해 해당 파일을 제외하고 있습니다.

## 🔗 관련 문서
* [**🏠 메인 페이지로 돌아가기 (README.md)**](../README.md)
* [**🚀 시작하기 (setup.md)**](./setup.md)
    * 요구 사항, 설치 방법 및 환경 변수 설정 안내
* [**📜 명령어 요약 (commands.md)**](./commands.md)
    * 관리자 및 일반 유저가 사용할 수 있는 전체 명령어 목록