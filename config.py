import os

modules = {
    "news_module": {
        "reddit_client_id": os.getenv("REDDIT_CLIENT_ID"),
        "reddit_client_secret": os.getenv("REDDIT_CLIENT_SECRET"),
        "reddit_user_agent": "MyNewsBot/1.0"
    }
}