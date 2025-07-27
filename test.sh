#!/bin/bash
# Simple shell wrapper for the Python test runner
# This provides an even simpler interface for running tests

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🧪 Nunyakata Test Runner${NC}"
echo -e "${CYAN}==============================${NC}"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

# Run the Python test runner with all arguments passed through
echo -e "${BLUE}Running: python3 run_tests.py $@${NC}"
echo ""

python3 run_tests.py "$@"
exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests completed successfully!${NC}"
else
    echo -e "${RED}❌ Some tests failed. Check output above for details.${NC}"
fi

exit $exit_code
