#!/bin/bash
# Build script to compile TypeScript files

echo "Compiling TypeScript..."
npx tsc

if [ $? -eq 0 ]; then
  echo "✓ TypeScript compilation successful"
else
  echo "✗ TypeScript compilation failed"
  exit 1
fi
