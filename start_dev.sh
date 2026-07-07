#!/bin/bash

module purge
module load gcc/12.2.0
module load python311

source ~/nlp_research_module/sglang_env/bin/activate

cd ~/nlp_research_module/extractor_pro/extractor-pro

export PYTHONPATH=$(pwd)

echo
echo "=============================="
echo "Extractor-Pro Development Ready"
echo "Project : $(pwd)"
echo "Python  : $(which python)"
echo "=============================="
echo
