# 개발 및 브랜치 규칙

이 프로젝트는 Git Flow와 Git worktree를 사용합니다.

- `main`: 안정된 릴리스 브랜치. 직접 커밋하지 않습니다.
- `develop`: 통합 브랜치이자 기본 브랜치.
- `feature/<name>`: `develop`에서 분기하고, 완료 후 PR로 `develop`에 병합합니다.
- `release/<version>`: 릴리스 안정화용이며 `main`과 `develop`에 반영합니다.
- `hotfix/<name>`: `main`에서 긴급 수정 후 `main`과 `develop`에 반영합니다.

브랜치마다 별도 worktree를 사용하고, 하나의 브랜치를 여러 worktree에서 동시에 체크아웃하지 않습니다.

현재 작업 폴더:

- `develop`: `C:/project/tic-tac-toe`
- `main`: `C:/project/tic-tac-toe-main`
- `feature/tic-tac-toe-game`: `C:/project/tic-tac-toe-feature-game`

```powershell
git worktree list
git worktree add -b feature/example C:/project/tic-tac-toe-feature-example develop
git worktree remove C:/project/tic-tac-toe-feature-example
```

병합 전 테스트를 실행합니다:

```powershell
python -m unittest discover -s tests -v
```
