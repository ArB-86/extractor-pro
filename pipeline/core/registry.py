class Registry:

    def __init__(self):

        self.stages=[]

    def register(self, stage):

        self.stages.append(stage)

    def build(self):

        return self.stages
