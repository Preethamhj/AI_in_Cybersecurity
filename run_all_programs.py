from __future__ import annotations

import contextlib
import io
import os
import runpy
import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_WEEKS = [f"week{i}" for i in range(1, 14)]


def run_program(week_dir: Path, program: Path) -> tuple[int, str]:
    output = io.StringIO()
    exit_code = 0
    image_index = 1

    os.environ.setdefault("MPLBACKEND", "Agg")
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    original_show = plt.show

    def save_show(*args, **kwargs):
        nonlocal image_index
        for figure_number in plt.get_fignums():
            figure = plt.figure(figure_number)
            image_path = week_dir / f"result_image_{image_index:02d}.png"
            while image_path.exists():
                image_index += 1
                image_path = week_dir / f"result_image_{image_index:02d}.png"
            figure.savefig(image_path, bbox_inches="tight", dpi=150)
            print(f"[saved image] {image_path.name}")
            image_index += 1
        plt.close("all")

    plt.show = save_show

    old_cwd = Path.cwd()
    old_argv = sys.argv[:]
    try:
        os.chdir(week_dir)
        sys.argv = [str(program)]
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                runpy.run_path(str(program), run_name="__main__")
            except SystemExit as exc:
                if isinstance(exc.code, int):
                    exit_code = exc.code
                elif exc.code:
                    exit_code = 1
                    print(exc.code)
            except Exception:
                exit_code = 1
                traceback.print_exc()
            finally:
                if plt.get_fignums():
                    save_show()
    finally:
        plt.show = original_show
        sys.argv = old_argv
        os.chdir(old_cwd)

    return exit_code, output.getvalue()


def main() -> int:
    overall_exit = 0
    weeks = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_WEEKS
    for week in weeks:
        week_dir = ROOT / week
        program = week_dir / f"p{week.removeprefix('week')}.py"
        result_file = week_dir / "result.txt"

        if not program.exists():
            result_file.write_text(f"Program not found: {program.name}\n", encoding="utf-8")
            overall_exit = 1
            continue

        exit_code, captured = run_program(week_dir, program)
        header = (
            f"Program: {program.name}\n"
            f"Working directory: {week_dir}\n"
            f"Exit code: {exit_code}\n"
            f"{'=' * 72}\n"
        )
        result_file.write_text(header + captured, encoding="utf-8")
        print(f"{week}: {program.name} -> exit {exit_code}")
        if exit_code != 0:
            overall_exit = exit_code

    return overall_exit


if __name__ == "__main__":
    raise SystemExit(main())
