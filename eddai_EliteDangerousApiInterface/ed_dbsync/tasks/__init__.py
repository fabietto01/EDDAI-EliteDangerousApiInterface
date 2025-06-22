from eddai_EliteDangerousApiInterface.celery import app
from .analyst import AnalystTasck
from .capiJournalSync import CapiJournalSync

app.register_task(AnalystTasck())
app.register_task(CapiJournalSync())