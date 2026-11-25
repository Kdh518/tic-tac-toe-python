# 틱택토

Python 표준 라이브러리와 Tkinter로 만든 데스크톱 틱택토 게임입니다.

## 실행

Python 3.10 이상에서 프로젝트 폴더의 PowerShell을 열고 실행하세요:

```powershell
python .\app.py
```

## 기능

- 2인 로컬 대전 또는 컴퓨터 대전
- 컴퓨터는 minimax 전략을 사용하며 최선의 수를 둡니다.
- 승리·무승부 판정, 새 게임, 점수 초기화
- 키보드 `1`~`9`로 칸 선택, `R`로 새 게임
- 점수판은 모드를 바꾸면 초기화됩니다.

## 테스트

```powershell
python -m unittest discover -s tests -v
```

## 브랜치 관리

Git Flow와 Git worktree를 사용합니다. `main`은 안정 버전, `develop`은 통합 브랜치이며, 작업 규칙은 [CONTRIBUTING.md](CONTRIBUTING.md)에 있습니다.
