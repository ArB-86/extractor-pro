from dataclasses import asdict

from pipeline.dataset_builder.schema import DatasetRecord


class DatasetBuilder:

    def build(self, questions):

        dataset=[]

        for q in questions:

            r=DatasetRecord()

            for k,v in asdict(r).items():

                if hasattr(q,k):
                    setattr(r,k,getattr(q,k))

            dataset.append(r)

        return dataset
