#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Run cProfile for: "
echo "V0: 0"
echo "V1: 1"
echo "V2: 2"
echo "Open Last Profiling results: p"

read -p "Select a version: " VERSION

# --- CONFIGURATION ---
PYTHON_SCRIPT="main.py"
RESULTS_DIR="./results/"
OUTPUT_FILE="${RESULTS_DIR}V${VERSION}_profile_results.prof"
VALID_OPTIONS=(0 1 2 p P)
IS_VALID=false
# ---------------------

# case $VERSION in
#   0)
#     echo "🚀 Starting cProfile on ${PYTHON_SCRIPT} V${VERSION}"
#     ;;
#   1)
#     echo "🚀 Starting cProfile on ${PYTHON_SCRIPT} V${VERSION}"
#     ;;
#   *)
#     echo "❌ Invalid option: '$VERSION'. Please enter 0, 1, or quit."
#     exit 1
#     ;;
# esac

# Check version with regex
# if [[ "$VERSION" =~ ^[0-2]$ ]]; then
#   echo "🚀 Starting cProfile on ${PYTHON_SCRIPT} V${VERSION}"
# else 
#   echo "❌ Invalid option: '$VERSION'. Please enter 0, 1, or quit."
#   exit 1

# Check version with loop
for opt in ${VALID_OPTIONS[@]}; do
  if [ "$opt" == "$VERSION" ]; then
    IS_VALID=true
    break
  fi
done

if [ "$IS_VALID" == false ]; then
   echo "❌ Invalid option: '$VERSION'." 
   exit 1
fi

case $VERSION in
  [Pp])
    echo "🔍 Scanning '$RESULTS_DIR' for profiling files..."
    if [ ! -d "$RESULTS_DIR" ]; then
      echo "❌ Error: Directory '$SEARCH_DIR' does not exist."
      exit 1
    fi 

    find $SEARCH_DIR -type f -name "*.prof"
    
    read -p "Input File Name: " FILE_NAME

    if [ ! -f "$FILE_NAME" ]; then
      echo "❌ Error: File'$FILE_NAME' does not exist."
      exit 1
    else
      echo "🚀 Opening last profiling results..."
      snakeviz "${FILE_NAME}"
      exit 0
    fi
    ;;
  *)
    # Run cProfile and output binary data to the specified file
    python -m cProfile -o "${OUTPUT_FILE}" "${PYTHON_SCRIPT}" 1 "${VERSION}"
    
    if [ -f "${OUTPUT_FILE}" ]; then
        echo "✅ Profiling complete!"
        echo "💾 Raw binary statistics saved to: ${OUTPUT_FILE}"
        echo ""
        echo "💡 To inspect the results in your terminal, run:"
        echo "   python3 -m pstats ${OUTPUT_FILE}"
        echo ""
        echo "📊 To view the interactive browser visualization, run:"
        echo "   snakeviz ${OUTPUT_FILE}"
    else
        echo "❌ Error: Failed to generate profile data."
        exit 1
    fi
    ;;
esac
