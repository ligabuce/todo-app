import uuid

class Todo:
    def __init__(self, task=None, status=None):
        self.id = str(uuid.uuid4())[:8]
        self.task = task
        if status is not None:
            self.status = status
        else:
            self.status = False

