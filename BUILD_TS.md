# Building TypeScript

This project uses TypeScript for frontend development. The TypeScript source file (`form-handler.ts`) is compiled to JavaScript (`form-handler.js`), which the browser loads.

## Option 1: Use Pre-compiled JavaScript (Ready Now)

The `form-handler.js` file is already compiled and ready to use. **No setup needed!** The app works immediately.

## Option 2: Development with TypeScript

To modify the TypeScript source and auto-compile during development:

### Install Node.js and npm
- Download and install from https://nodejs.org/

### Setup

```bash
# Install dependencies
npm install

# Start watch mode - automatically compiles TS → JS on file changes
npm run watch

# Or use esbuild for faster compilation
npm run watch:esbuild
```

## Workflow

1. **Edit** `src/static/form-handler.ts` (TypeScript source)
2. **Watch** automatically compiles to `src/static/form-handler.js`
3. **Refresh** browser - new JavaScript is loaded
4. Done! No manual compilation needed

## Commands

```bash
# Compile TypeScript once (using tsc)
npm run build

# Compile once (using esbuild - faster)
npm run build:esbuild

# Watch mode (auto-compile on changes) - use during development
npm run watch
npm run watch:esbuild
```

## File Structure

- `src/static/form-handler.ts` ← **Edit this** (TypeScript source)
- `src/static/form-handler.js` ← **Auto-generated** (Compiled JavaScript)
- `tsconfig.json` ← TypeScript configuration

## How It Works

1. You edit the TypeScript file (`form-handler.ts`)
2. NPM script compiles it to JavaScript (`form-handler.js`)
3. HTML loads `form-handler.js` in the browser
4. The JavaScript runs in the browser

## Why This Approach?

- **TypeScript Source**: Provides type safety and better development experience
- **Compiled JavaScript**: Browsers can only run JavaScript, not TypeScript
- **Auto-compile**: Watch mode means you don't have to manually compile
- **Pre-built JS**: The JS file is already included, so the app works without npm

## Quick Start

```bash
# Get started
npm install
npm run watch

# Now edit src/static/form-handler.ts and refresh browser!
```

## Notes

- Always run `npm run watch` during development
- Commit the TypeScript source to version control
- The compiled JS is generated automatically, no need to commit it
- Source maps in JS enable debugging with original TypeScript code

