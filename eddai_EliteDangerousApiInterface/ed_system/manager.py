from django.db import models
from ed_core.functions import Distanza3D
from django.db.models.functions import Round

class SystemQuerySet(models.QuerySet):

    def distance_from_system(self, system):
        return self.annotate(
            distance_st=models.ExpressionWrapper(
                Round(
                    Distanza3D(
                        models.F('coordinate'),
                        point=system.coordinate
                    ),
                    3
                ),
                output_field=models.FloatField()
            )
        )
    
    def view_system_control_faction(self):
        return self.annotate(
            conrolling_faction_view=models.FilteredRelation(
                "conrollingFaction__ed_bgs_minorfactioninsystems",
                condition=models.Q(conrollingFaction__ed_bgs_minorfactioninsystems__system_id=models.F('id'))
            )
        )

    def view_system_power(self):
        return self.select_related('ed_bgs_PowerInSystem_related')

class SystemManager(models.Manager.from_queryset(SystemQuerySet)):
    pass