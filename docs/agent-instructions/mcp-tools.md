# MCP Tools

## Overview

These tools extend OpenCode capabilities. Use them as needed for specific tasks.

## Available Tools

### playwright

- Operate a web browser: navigate, click around, take snapshots
- Use this whenever you want to look at a web page
- When working on a web app, run the local web server and interact with the app
- **Always take a look using playwright** so you know how the results of your work look

### markitdown

- Convert various file formats to markdown
- Useful for reading files not supported natively by the model

### exa

- Run web searches
- Always better to search the web than to rely on pre-trained knowledge which may be outdated
- Retrieve content in a format easy for ingestion

### thinking

- If you are not a native reasoning model (i.e., you do not produce internal chains-of-thought automatically), you **MUST** use the thinking tool

### context7

- Read the documentation for many libraries and tools
- When asked to use a library, framework, or tool, review its documentation first with Context7

## Usage Notes

- Each tool has specific use cases - use the right tool for the task
- Don't use playwright if you just need to fetch a URL (use curl or exa instead)
- Don't use context7 for general web searches (use exa instead)