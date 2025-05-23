# accountant-telegram-bot
Super simple accountant telegram bot for manage one simple variable that changes when receive numbers.

## Getting started

To manually create a virtualenv on MacOS and Linux:

```bash
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

Make sure you have read-write permissions to run the bot later.
```bash
source .venv/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies.

```bash
pip install -r requirements.txt
```

Rename the file `env.example.py` to `env.py` and change its internal values.

Run it.
```bash
python __init__.py
```

### With docker

```bash
# Create storage folder
mkdir storage

# Launch it
docker build . -t acc && docker run --restart=always -d -v $(pwd)/storage:/app/storage acc
```