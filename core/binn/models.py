from django.db import models
import sys
import os
from config.settings import BASE_DIR
# Create your models here.

IDENTF = [
    ("I", "Información"),
    ("R", "Reportes"),
    ("A", "Advertencias"),
    ("E", "Error"),
]
class BinnacleMessages(models.Model):
    identifier=models.CharField(max_length=1,choices=IDENTF)
    identifier_message=models.CharField(max_length=50)
    reason=models.CharField(max_length=50)
    timedate=models.DateTimeField(auto_now_add=True)
    def info(id_m,reason):
        BinnacleMessages.objects.create(
            identifier="I",
            identifier_message=id_m,
            reason=reason,
        )
    def error(e):
        exc_type, exc_value,exc_traceback=sys.exc_info()
        r_r = os.path.relpath(exc_traceback.tb_frame.f_code.co_filename, BASE_DIR)
        BinnacleMessages.objects.create(
            identifier="E",
            identifier_message=f"Tipo:{exc_type.__name__}-----Fichero:{r_r}------Linea:{exc_traceback.tb_lineno}",
            reason=f"{e}",
        )
    def warning(id_m,reason):
        BinnacleMessages.objects.create(
            identifier="A",
            identifier_message=id_m,
            reason=reason,
        )
    def report(id_m,reason):
        BinnacleMessages.objects.create(
            identifier="R",
            identifier_message=id_m,
            reason=reason,
        )