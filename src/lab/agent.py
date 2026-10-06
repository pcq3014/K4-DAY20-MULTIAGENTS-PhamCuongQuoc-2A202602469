"""GUIDE Phần 1 - Dựng tác tử (agent) bằng Deep Agents.   >>> SINH VIÊN CÀI ĐẶT make_backend VÀ build_agent <<<

Pseudo-code: guides/pseudocode/01_agent.md
Kiểm tra:    pytest tests/test_02_agent.py
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend
from deepagents.backends.protocol import ExecuteResponse

from .model import make_model
from .subagents import get_subagents

# ---- CÓ SẴN, KHÔNG SỬA: system prompt dùng chung cho mọi sinh viên (để đường cơ sở so sánh được) ----
PATHS_NOTE = (
    "PATHS: every path is relative to the sandbox root and never starts with '/'. "
    "The task files are in the folder workspace/ (for example workspace/app.log). "
    "Use exactly this relative form both in the file tools and in the shell (execute); "
    "the shell starts in the sandbox root. "
)
BASE_PROMPT = (
    "You are an engineering assistant working in a sandbox. "
    + PATHS_NOTE
    + "Use the shell to run Python and tests. "
    "When you are done, reply with a short summary that mentions only files you really created or changed."
)
SKILLS_NOTE = (
    " Skills are in the folder skills/ (one sub-folder per skill with a SKILL.md). "
    "As your FIRST action, read the SKILL.md of every skill whose description could apply to the task, "
    "then follow them. Never modify skills/."
)
SUBAGENTS_NOTE = (
    " You have specialised subagents (see the description of the task tool). "
    "For anything beyond a trivial step, delegate to a suitable subagent and put ALL the task rules and file paths "
    "in the delegation message, because a subagent sees only what you send. "
    "Check what a subagent returns before you rely on it."
)
# --------------------------------------------------------------------------------------------------


def make_backend(sandbox: Path):
    """Tạo backend (môi trường thực thi) cho tác tử.

    Yêu cầu:
      - Thư mục gốc (root_dir) là `sandbox`; đường dẫn tương đối `workspace/...` và `skills/...`
        phải dùng được ở CẢ công cụ tệp lẫn shell (shell chạy với thư mục làm việc = `sandbox`).
      - Tác tử chạy được lệnh shell và gọi được `python` (cần đặt PATH).
      - KHÔNG chuyển biến môi trường của bạn vào shell của tác tử (khóa API không được lộ).
    """
    python_dir = str(Path(sys.executable).parent)
    kwargs = dict(root_dir=sandbox, virtual_mode=True, inherit_env=False, timeout=120)
    if sys.platform == "win32":
        # cmd.exe không hiểu cú pháp POSIX -> chạy lệnh bằng bash của Git for Windows.
        # Lưu ý: KHÔNG cô lập (shell thấy cả ổ đĩa); chỉ để thử nhanh, chạy chính thức trong Docker.
        bash = _find_git_bash()
        env = {
            "PATH": os.pathsep.join([python_dir, str(Path(bash).parent)]),
            "HOME": str(sandbox),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUTF8": "1",
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", r"C:\Windows"),   # Python trên Windows cần biến này
        }
        return _PrefixShellBackend([bash, "-c"], env=env, **kwargs)
    env = {
        "PATH": python_dir + ":/usr/local/bin:/usr/bin:/bin",
        "HOME": str(sandbox),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    agent_user = os.getenv("LAB_AGENT_USER")
    if agent_user and os.geteuid() == 0:
        # Cô lập (dùng trong Docker): runner chạy bằng root, lệnh shell của tác tử chạy bằng user không đặc quyền,
        # nên không đọc được repo (mount ở /root/lab, /root có quyền 700): bộ chấm, tác vụ đánh giá, kết quả cũ.
        import pwd
        user = pwd.getpwnam(agent_user)
        prefix = ["setpriv", f"--reuid={user.pw_uid}", f"--regid={user.pw_gid}", "--clear-groups", "--", "/bin/sh", "-c"]
        return _PrefixShellBackend(prefix, open_sandbox=True, env=env, **kwargs)
    return LocalShellBackend(env=env, **kwargs)


def _open_sandbox_to_agent(sandbox: Path) -> None:
    """Cho user của tác tử ghi được vào sandbox (trừ skills/, chỉ đọc).

    Bỏ qua symlink: nếu không, tác tử có thể tạo `ln -s /root x` để root chmod hộ thư mục bên ngoài.
    """
    for dirpath, dirnames, filenames in os.walk(sandbox, followlinks=False):
        d = Path(dirpath)
        read_only = d.relative_to(sandbox).parts[:1] == ("skills",)
        if not d.is_symlink():
            d.chmod(0o755 if read_only else 0o777)
        for name in filenames:
            f = d / name
            if not f.is_symlink():
                f.chmod(0o644 if read_only else 0o666)


def _find_git_bash() -> str:
    """Tìm bash của Git for Windows (tránh System32/bash.exe của WSL)."""
    git = shutil.which("git")
    if git:
        for cand in ("usr/bin/bash.exe", "bin/bash.exe"):
            p = Path(git).resolve().parent.parent / cand
            if p.exists():
                return str(p)
    bash = shutil.which("bash")
    if not bash:
        raise RuntimeError("Không tìm thấy bash. Cài Git for Windows, hoặc chạy lab trong WSL/Docker.")
    return bash


class _PrefixShellBackend(LocalShellBackend):
    """LocalShellBackend chạy lệnh bằng `prefix + [command]` (không qua shell mặc định của hệ điều hành)."""

    def __init__(self, prefix: list[str], open_sandbox: bool = False, **kwargs):
        super().__init__(**kwargs)
        self._prefix = prefix
        self._open_sandbox = open_sandbox

    def execute(self, command: str, *, timeout: int | None = None) -> ExecuteResponse:
        if not command or not isinstance(command, str):
            return ExecuteResponse(output="Error: Command must be a non-empty string.", exit_code=1, truncated=False)
        effective_timeout = timeout if timeout is not None else self._default_timeout
        if self._open_sandbox:   # tệp do công cụ tệp (root) vừa tạo cũng phải ghi được từ shell của tác tử
            _open_sandbox_to_agent(self.cwd)
        try:
            result = subprocess.run(
                [*self._prefix, command], capture_output=True, stdin=subprocess.DEVNULL, text=True,
                encoding="utf-8", errors="replace", timeout=effective_timeout, env=self._env, cwd=str(self.cwd),
            )
        except subprocess.TimeoutExpired:
            return ExecuteResponse(output=f"Error: Command timed out after {effective_timeout} seconds.",
                                   exit_code=124, truncated=False)
        except Exception as e:  # noqa: BLE001
            return ExecuteResponse(output=f"Error executing command ({type(e).__name__}): {e}", exit_code=1, truncated=False)
        parts = [result.stdout] if result.stdout else []
        if result.stderr:
            parts.extend(f"[stderr] {line}" for line in result.stderr.strip().split("\n"))
        output = "\n".join(parts) if parts else "<no output>"
        truncated = len(output) > self._max_output_bytes
        if truncated:
            output = output[: self._max_output_bytes] + f"\n\n... Output truncated at {self._max_output_bytes} bytes."
        if result.returncode != 0:
            output = f"{output.rstrip()}\n\nExit code: {result.returncode}"
        return ExecuteResponse(output=output, exit_code=result.returncode, truncated=truncated)


def build_agent(sandbox: Path, mode: str = "single", use_skills: bool = False, model=None):
    """Tạo tác tử Deep Agents.

    Tham số:
      sandbox:    thư mục chứa `workspace/` (và `skills/` nếu có).
      mode:       "single"    -> tác tử mặc định (có subagent `general-purpose` sẵn của Deep Agents)
                  "subagents" -> thêm các subagent từ `get_subagents()` (nối PATHS_NOTE vào `system_prompt` của MỖI subagent,
                                 vì subagent không nhận BASE_PROMPT) và thêm SUBAGENTS_NOTE vào prompt chính
      use_skills: True -> nạp thư mục "/skills/" qua tham số `skills=` của create_deep_agent
                  và thêm SKILLS_NOTE vào prompt.
      model:      mô hình ngôn ngữ; None -> dùng `make_model()`.
    mode không hợp lệ -> ném ValueError.
    Trả về: đồ thị (graph) đã biên dịch, gọi bằng `.invoke({"messages": [...]})`.
    """
    if mode not in ("single", "subagents"):
        raise ValueError(f"unknown mode: {mode!r} (expected 'single' or 'subagents')")

    kwargs = {}
    prompt = BASE_PROMPT
    if mode == "subagents":
        # subagent không nhận BASE_PROMPT -> nối quy ước đường dẫn vào từng subagent
        kwargs["subagents"] = [{**sub, "system_prompt": sub["system_prompt"] + " " + PATHS_NOTE} for sub in get_subagents()]
        prompt += SUBAGENTS_NOTE
    if use_skills:
        kwargs["skills"] = ["/skills/"]
        prompt += SKILLS_NOTE

    return create_deep_agent(
        model=model or make_model(),
        system_prompt=prompt,
        backend=make_backend(sandbox),
        **kwargs,
    )
