from celery import Celery

app:Celery = locals().get("app", None)

if not app is None:

    @app.on_after_configure.connect
    def setup_periodic_tasks(sender, *args, **kwargs):
        x =1
        pass
