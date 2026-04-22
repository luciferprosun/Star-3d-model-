# Star-3d-model-

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
