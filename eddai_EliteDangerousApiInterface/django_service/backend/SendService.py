from ..celey import Service

from ..models import Service

class SendService(Service):

    def __init__(self, pre_save:Service, post_save:Service) -> None:
        super().__init__()
        self.pre_save = pre_save
        self.post_save = post_save
        