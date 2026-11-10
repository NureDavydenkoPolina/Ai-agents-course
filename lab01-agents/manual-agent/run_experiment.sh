#!/usr/bin/env bash
# Використання: bash run_experiment.sh oneshot|agent [номери запитів 1-5]
mode="$1"; shift
mkdir -p experiments
types=(A B C D E)
queries=(
  "Розкажи про оператор menu у Ren'Py"
  "Порівняй scene і show у Ren'Py"
  "Чим відрізняються jump, call і return у Ren'Py?"
  "Опиши оператор screen у Ren'Py"
  "Що таке Ren'Py і для чого він потрібен?"
)
if [ "$#" -gt 0 ]; then idx=("$@"); else idx=(1 2 3 4 5); fi
first=1
for n in "${idx[@]}"; do
  i=$((n-1))
  if [ "$first" -eq 0 ]; then echo "[пауза 65 с: ліміт 5 запитів на хвилину]"; sleep 65; fi
  first=0
  out="experiments/q${n}_${types[$i]}_${mode}.txt"
  echo "=== ${types[$i]}: ${queries[$i]} ($mode) ==="
  uv run python -W ignore main.py "${queries[$i]}" --mode "$mode" 2>&1 | tee "$out"
done
