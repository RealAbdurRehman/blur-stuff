import tempfile
import subprocess
from pathlib import Path


def to_pdf(data, extension):
    with tempfile.TemporaryDirectory() as tmp:
        input_file = Path(tmp) / f"input{extension}"
        output_dir = Path(tmp)
        input_file.write_bytes(data)

        subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(output_dir),
                str(input_file),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        pdf = output_dir / "input.pdf"
        return pdf.read_bytes()
