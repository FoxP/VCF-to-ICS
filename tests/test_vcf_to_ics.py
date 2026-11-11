"""Tests for vcf_to_ics.py (run with pytest from the repo root)."""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "vcf_to_ics.py"


def run_converter(input_file, output_file, calendar="TestCal"):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "-i", str(input_file),
         "-o", str(output_file), "-n", calendar],
        capture_output=True,
        text=True,
    )


def test_latin1_input_converts_without_traceback(tmp_path):
    vcf = tmp_path / "contacts.vcf"
    vcf.write_bytes(
        "BEGIN:VCARD\r\nVERSION:3.0\r\nFN:Andr\xe9 Dupont\r\n"
        "BDAY:1980-05-01\r\nEND:VCARD\r\n".encode("latin-1")
    )
    out = tmp_path / "out.ics"
    result = run_converter(vcf, out)
    assert result.returncode == 0
    assert "Traceback" not in result.stderr
    content = out.read_text(encoding="utf-8")
    assert "Andr\xe9 Dupont" in content
    assert "DTSTART:19800501" in content


def test_utf8_input_still_converts(tmp_path):
    vcf = tmp_path / "contacts.vcf"
    vcf.write_text(
        "BEGIN:VCARD\nVERSION:3.0\nFN:John Doe\n"
        "BDAY:2018-12-01\nEND:VCARD\n",
        encoding="utf-8",
    )
    out = tmp_path / "out.ics"
    result = run_converter(vcf, out)
    assert result.returncode == 0
    content = out.read_text(encoding="utf-8")
    assert "John Doe" in content
    assert "DTSTART:20181201" in content
