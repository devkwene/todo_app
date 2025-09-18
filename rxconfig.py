
import reflex as rx
from reflex.plugins.sitemap import SitemapPlugin

config = rx.Config(
    app_name="todo_app",
    db_url="postgresql://todo_user:123@localhost:5432/todo_app",
    plugins=[SitemapPlugin()]
)