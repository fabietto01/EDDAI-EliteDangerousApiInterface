class EDInfoRouter:
    """
    Un router per controllare tutte le operazioni del database sui 
    modelli nelle applicazione ed_system.
    """
    route_app_labels = {
        "ed_system","ed_body","ed_bgs","ed_core","ed_economy","ed_station","eddn",'ed_material',
        'ed_mining'
    }

    def db_for_read(self, model, **hints):
        """
        I tentativi di leggere dei modelli in 'route_app_labels' vanno a ed_info.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'ed_info'
        return None

    def db_for_write(self, model, **hints):
        """
        I tentativi di scrivere dei modelli in 'route_app_labels' vanno a ed_info.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'ed_info'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Consenti relazioni se è coinvolto un modello di 
        una app presenre in 'route_app_labels'
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Assicurati che le app in 'route_app_labels' appaiano solo nel database 'ed_info'.
        """
        if app_label in self.route_app_labels:
            return db == 'ed_info'
        return None