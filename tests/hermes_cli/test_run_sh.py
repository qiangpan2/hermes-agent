from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RUN_SCRIPT = REPO_ROOT / "run.sh"


def test_run_sh_links_rapid_plugin_into_hermes_home(tmp_path):
    repo_copy = tmp_path / "repo"
    repo_copy.mkdir()

    shutil.copy2(RUN_SCRIPT, repo_copy / "run.sh")
    shutil.copy2(REPO_ROOT / ".env.example", repo_copy / ".env.example")
    shutil.copytree(REPO_ROOT / "RAPID-Plugins", repo_copy / "RAPID-Plugins")

    fake_bin = tmp_path / "fake-bin"
    fake_bin.mkdir()
    fake_uv = fake_bin / "uv"
    fake_uv.write_text(
        """#!/usr/bin/env bash
set -e

case "$1" in
  venv)
    target="$2"
    mkdir -p "$target/bin"
    cat > "$target/bin/activate" <<'EOF'
# fake activate
EOF
    ;;
  pip)
    ;;
  run)
    {
      printf 'HERMES_HOME=%s\n' "${HERMES_HOME:-}"
      printf 'HERMES_ENABLE_PROJECT_PLUGINS=%s\n' "${HERMES_ENABLE_PROJECT_PLUGINS:-}"
      printf 'ARGS=%s\n' "$*"
    } > "$PWD/gateway-env.txt"
    ;;
  *)
    echo "unexpected uv args: $*" >&2
    exit 1
    ;;
esac
""",
        encoding="utf-8",
    )
    fake_uv.chmod(0o755)

    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}:{env['PATH']}"

    result = subprocess.run(
        ["bash", str(repo_copy / "run.sh")],
        cwd=repo_copy,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    env_file = repo_copy / ".hermes" / ".env"
    assert env_file.exists()

    env_content = env_file.read_text(encoding="utf-8")
    assert "RAPID_RUNTIME_BASE_URL=http://127.0.0.1:3000" in env_content

    plugin_link = repo_copy / ".hermes" / "plugins" / "rapid"
    assert plugin_link.is_symlink()
    assert plugin_link.resolve() == (repo_copy / "RAPID-Plugins").resolve()

    gateway_env = (repo_copy / "gateway-env.txt").read_text(encoding="utf-8")
    assert f"HERMES_HOME={repo_copy / '.hermes'}" in gateway_env
    assert "HERMES_ENABLE_PROJECT_PLUGINS=" in gateway_env
    assert "ARGS=run hermes gateway run" in gateway_env
