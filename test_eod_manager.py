import sys, os, tempfile, shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eod_manager
from eod_manager import validate_project_name, assert_within_base_dir

results = []

# Setup: isolated temporary directory so tests never touch the real reports dir
_tmp = tempfile.mkdtemp(prefix="eod_test_")
_orig_base = eod_manager.BASE_DIR
eod_manager.BASE_DIR = Path(_tmp)

try:
    # T1: path traversal rejected
    try:
        validate_project_name("../../.ssh/authorized_keys")
        results.append("FAIL  T1: path traversal -- did not raise")
    except SystemExit:
        results.append("PASS  T1: path traversal raises SystemExit")

    # T2: glob wildcard rejected
    try:
        validate_project_name("my-*-proj")
        results.append("FAIL  T2: glob wildcard -- did not raise")
    except SystemExit:
        results.append("PASS  T2: glob wildcard raises SystemExit")

    # T3: valid names pass
    try:
        for n in ["my-project", "JIRA101", "proj_v2"]:
            validate_project_name(n)
        results.append("PASS  T3: valid names accepted")
    except SystemExit as e:
        results.append(f"FAIL  T3: valid name rejected: {e}")

    # T4: assert_within_base_dir rejects path outside BASE_DIR
    try:
        assert_within_base_dir(Path("/tmp/evil.md"))
        results.append("FAIL  T4: outside path -- did not raise")
    except SystemExit:
        results.append("PASS  T4: outside path rejected by sandbox")

    # T5: valid sub-path is accepted by assert_within_base_dir (calls production logic directly)
    sub = eod_manager.BASE_DIR / "2026-03-14" / "eod-report-ok-01.md"
    try:
        assert_within_base_dir(sub)
        results.append("PASS  T5: valid sub-path passes sandbox")
    except SystemExit as e:
        results.append(f"FAIL  T5: valid sub-path rejected: {e}")

    # T6: content-size cap — temporarily lower the limit to avoid a >100 MB allocation
    _orig_max = eod_manager.MAX_CONTENT_BYTES
    eod_manager.MAX_CONTENT_BYTES = 10
    try:
        try:
            eod_manager.save_report("testproj", "x" * 11)
            results.append("FAIL  T6: oversized content -- did not raise")
        except SystemExit:
            results.append("PASS  T6: oversized content raises SystemExit")
    finally:
        eod_manager.MAX_CONTENT_BYTES = _orig_max

    # T7: file written with 0o600 permissions
    path = eod_manager.save_report("testproj-sec", "hello security test")
    mode = oct(os.stat(path).st_mode & 0o777)
    if mode == oct(0o600):
        results.append("PASS  T7: file permissions are 0o600")
    else:
        results.append(f"FAIL  T7: expected 0o600, got {mode}")

finally:
    eod_manager.BASE_DIR = _orig_base
    shutil.rmtree(_tmp, ignore_errors=True)

print("\n".join(results))
failed = [r for r in results if r.startswith("FAIL")]
sys.exit(1 if failed else 0)
