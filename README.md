# Star-3d-model-

Interactive solar interior model built as a standalone Three.js page.

Public page:

```text
https://luciferprosun.github.io/Star-3d-model-/Model.html
```

Run the model with access logging:

```bash
python3 server.py
```

Then open:

```text
http://127.0.0.1:8000/Model.html
```

Each request is printed to the terminal and appended to `access.log` as JSON with:
- client IP
- timestamp
- path
- user-agent
- forwarded headers

Gemini code review:

```text
GitHub -> Settings -> Secrets and variables -> Actions -> New repository secret
Name: GEMINI_API_KEY
Value: your Gemini API key
```

Then run the `Gemini Code Review` workflow from the Actions tab, or let it run on `main` pushes and pull requests that touch the model files.
