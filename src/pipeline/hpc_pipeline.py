import os
import subprocess
from pathlib import Path


class HPCPipeline:

    def submit(self, pdf, output_dir):

        script = Path(output_dir) / "job.sh"

        script.write_text(
f"""#!/bin/bash
#PBS -N extractor
#PBS -l select=1:ncpus=16:ngpus=1
#PBS -l walltime=08:00:00

cd {os.getcwd()}

python -m src.cli extract "{pdf}" -o "{output_dir}"
"""
        )

        subprocess.run(
            ["qsub", str(script)],
            check=True,
        )
