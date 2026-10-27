# avoid-default-worldbuilding

세계관을 AI에게 맡길 때 시계공·시간 수리·등대의 비밀 같은 기본 설정을 피하도록 지시하는 Agent Skill이다.

A small, instruction-only skill for avoiding stock AI worldbuilding while
preserving explicit user choices, established canon and ordinary details.

실행부는 [SKILL.md](skills/avoid-default-worldbuilding/SKILL.md) 하나다.
데이터베이스나 API 연결 없이 사용한다. Python은 유지보수 검사에만 필요하다.
규칙은 모델 공통이고 특정 모델 버전의 성향을 단정하지 않는다.

## 무엇을 바꾸나

사용자가 지정하지 않은 **중심 설정**에 한해 시계공·시간 장치, 등대의 비밀,
기억 복원, 신비한 기록물, 꿈 세계, 고대 유물로 균형 복구, 예언된 구원자,
편의적인 차원 장치를 피한다. 정확한 조건은 SKILL.md의 WB01–WB08이 유일한 기준이다.

- “시간루프 게임을 만들어” → 시간루프를 유지한다. 허락하지 않은 다른 클리셰까지 덧붙이지 않는다.
- “세계관은 알아서 정해” → 목록과 겹치는 중심 설정을 다른 인과·역할·갈등으로 바꾼다.
- “시계가 배경에 있는 카페”, 번역, 기존 게임 버그 수정 → 소재를 삭제하거나 세계관을 바꾸지 않는다.

고쳐야 할 중심 설정이 없으면 그대로 둔다. 수정할 때도 고정된 장소·인물·조작·분량은
유지한다. 시계공을 ‘크로노 엔지니어’로 부르는 식의 이름 바꾸기는 설정 변경으로 보지 않는다.

논문으로 확인한 소재와 편집 방침으로 추가한 패턴을
[근거 장부](skills/avoid-default-worldbuilding/references/EVIDENCE.md)에 구분했다.
**클리셰 회피는 독창성 보증도, 모든 모델에서의 빈도 순위도 아니다.**

## 설치 — Windows 11 / PowerShell

```powershell
git clone https://github.com/Legerdo/avoid-default-worldbuilding.git
Set-Location avoid-default-worldbuilding
```

저장소 루트에서 실행한다. 아래는 **프로젝트 단위** 설치이며 사용자 전역 설정을 바꾸지 않는다.
`C:\path\to\your-project`를 실제 대상 프로젝트로 바꾼다.

```powershell
$Project = 'C:\path\to\your-project'
# Claude Code: .claude / Codex: .agents / Gemini CLI: .gemini
$HostFolder = '.claude'
$Source = Join-Path $PWD 'skills\avoid-default-worldbuilding'
$Parent = Join-Path $Project "$HostFolder\skills"
$Target = Join-Path $Parent 'avoid-default-worldbuilding'
if (-not (Test-Path -LiteralPath $Project -PathType Container)) { throw '대상 프로젝트가 없다.' }
if (Test-Path -LiteralPath $Target) { throw '기존 설치가 있다. 변경분을 비교한 뒤 교체하라.' }
New-Item -ItemType Directory -Path $Parent -Force | Out-Null
Copy-Item -LiteralPath $Source -Destination $Target -Recurse
Get-Content -LiteralPath (Join-Path $Target 'SKILL.md') -Encoding UTF8 -TotalCount 8
```

Codex와 Gemini CLI는 `.agents/skills`를 공유할 수 있지만, 같은 스킬을 여러 경로에
중복 설치하지 않는다. 경로의 공식 근거는 [S3–S5](skills/avoid-default-worldbuilding/references/EVIDENCE.md)에 있다.

Claude Code에서는 `/avoid-default-worldbuilding`으로 명시 호출할 수 있다.
다른 호스트에서는 해당 스킬 선택 UI 또는 이름을 명시한 요청을 쓴다.
Gemini CLI의 `/skills list`로 발견 여부를 확인할 수 있다.
자동 발견과 자동 적용은 별개다. 처음에는 명시 호출하고 실제 활성화 기록을 확인한다.
일반 웹 채팅에 파일을 올렸다고 자동 설치되는 것은 아니다. 그런 환경에서는
SKILL.md 본문을 지침으로 직접 제공할 수 있지만 이는 네이티브 설치 검증과 다르다.

## 사용

```text
avoid-default-worldbuilding 스킬을 적용해서 2D 퍼즐 게임 콘셉트 하나를 만들어.
조작은 이동과 밀기뿐이고, 10분 안에 끝나야 한다. 세계관은 자율로 정해.
```

결과 형식, 언어, 분량은 원래 요청을 따른다. 후보 목록이나 검사 보고서를 강제로 출력하지 않는다.
일부러 해당 소재를 쓰고 싶으면 명시하면 된다. 별도의 설정 파일이나 허용 목록은 필요 없다.

## 유지보수

| 바꾸려는 것 | 수정 위치 |
| --- | --- |
| 적용 범위·예외·회피 패턴 | `skills/avoid-default-worldbuilding/SKILL.md` |
| 근거·근거의 한계 | `skills/avoid-default-worldbuilding/references/EVIDENCE.md` |
| 재발하면 안 되는 실제 사례 | `evals/cases.json` |
| 변경 이유·버전 | `CHANGELOG.md`, SKILL.md의 `metadata.version` |

규칙 추가 시 **막아야 할 사례와 허용해야 할 경계 사례를 한 쌍으로** 추가한다.
구체적인 절차는 [CONTRIBUTING.md](CONTRIBUTING.md)에 있다.
원칙은 규칙을 늘리는 것보다 불필요하게 막는 범위를 줄이는 것이다.

## 개발 검증과 배포 파일

사용자는 Python이 필요 없다. 아래는 저장소 기여자용이며 Python 3.11 이상을 사용한다.
Windows에서 PATH가 빠진 세션이라면 사용자 PATH만 세션에 추가한다.

```powershell
$env:PATH += ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
$env:PYTHONUTF8 = '1'
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe tools/check.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tools/package.py
```

`dist/`에 설치용 ZIP, 저장소 소스 ZIP, SHA256SUMS가 생성된다.
패키지는 파일 허용 목록으로 만들며 `.git`, 비밀키, 가상환경, 개인 실행 기록을 싣지 않는다.
`.github/workflows/ci.yml`은 Windows/Ubuntu 및 Python 3.11/3.13 검사를 정의한다.
실제 실행한 범위와 미실행 항목은 [v1.1.0 검증 기록](validation/v1.1.0.md)을 본다.
이전 기록은 [VALIDATION.md](VALIDATION.md)에 남겨 두었다.
**정적 검사 통과를 모델 행동 검증 통과로 취급하지 않는다.**

## 참고 프로젝트와 라이선스

v1.1.0의 문구는 [AI Slop Thresher](https://github.com/Burntgogi/ai-slop-thresher)를
참고해 다듬었다. 뜻과 조건 보존, 불필요한 수정 방지, 진단과 편집의 구분을 참고했으며
해당 프로젝트의 코드·프롬프트·예문을 가져오지는 않았다. 그 프로젝트는 한국어 윤문 도구이며,
여기서는 문체 교정 기능을 추가하지 않는다. 확인한 커밋과 라이선스는
[근거 장부의 S6](skills/avoid-default-worldbuilding/references/EVIDENCE.md)에 기록했다.

코드와 지침의 변경 이력은 [CHANGELOG.md](CHANGELOG.md), 원격 검사 결과는
[GitHub Actions](https://github.com/Legerdo/avoid-default-worldbuilding/actions)에서 확인한다.
자동 릴리스나 모델 API 호출은 없다.

[MIT](LICENSE). 외부 논문·자료는 링크와 요약만 제공하며 그 원문은 이 라이선스로 재배포하지 않는다.
