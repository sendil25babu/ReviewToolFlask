# Frontend TypeScript Setup

This project uses TypeScript for frontend development with automatic compilation.

## Quick Start (No Setup Needed)

The app works immediately with the pre-compiled JavaScript. Just run the Flask app - no npm installation required!

```bash
python src/main.py
```

The browser loads `form-handler.js` automatically.

## Development with TypeScript

If you want to modify the TypeScript source during development:

### 1. Install Node.js and npm
- Download from https://nodejs.org/
- Verify: `node --version` and `npm --version`

### 2. Install dependencies
```bash
npm install
```

### 3. Start auto-compilation
```bash
# TypeScript compiler watch mode (auto-compile on file changes)
npm run watch

# Or use esbuild for faster compilation
npm run watch:esbuild
```

### 4. Edit and develop
- Edit `src/static/form-handler.ts`
- Automatically compiles to `src/static/form-handler.js`
- Refresh browser to see changes

## Project Structure

```
src/
├── static/
│   ├── form-handler.ts      ← Edit this (TypeScript source)
│   └── form-handler.js      ← Auto-compiled (Browser loads this)
├── templates/
│   └── index.html
└── ...
tsconfig.json                ← TypeScript settings
package.json                 ← npm scripts
```

## Development Commands

```bash
# One-time compile
npm run build

# Auto-compile on file changes (use during development)
npm run watch

# Using esbuild (faster)
npm run build:esbuild
npm run watch:esbuild
```

## TypeScript Features

The project uses:
- **Strict type checking** - catches errors at compile time
- **Interfaces** - for API contracts (FormData, ApiResponse)
- **Async/await** - with proper error handling
- **DOM type safety** - HTMLInputElement, etc.
- **Source maps** - enables debugging with TypeScript code

## Workflow

| Task | Command |
|------|---------|
| Run app (no setup) | `python src/main.py` |
| Setup for development | `npm install` |
| Auto-compile TS | `npm run watch` |
| Compile once | `npm run build` |
| Faster compile | `npm run watch:esbuild` |

## Browser Requirements

- Modern browser (ES2020 support)
- Source maps in DevTools for TypeScript debugging
- No transpiler needed in browser (JavaScript is pre-compiled)

## Notes

- HTML loads `form-handler.js` (the compiled output)
- Edit `form-handler.ts` (the source)
- Compilation is automatic with watch mode
- Perfect for development with TypeScript benefits!

