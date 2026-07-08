from dataclasses import dataclass


@dataclass(slots=True)
class BenchmarkMetrics:

    true_positive: int = 0
    false_positive: int = 0
    false_negative: int = 0

    @property
    def precision(self):

        d = self.true_positive + self.false_positive

        return 0.0 if d == 0 else self.true_positive / d

    @property
    def recall(self):

        d = self.true_positive + self.false_negative

        return 0.0 if d == 0 else self.true_positive / d

    @property
    def f1(self):

        p = self.precision
        r = self.recall

        if p + r == 0:
            return 0.0

        return 2 * p * r / (p + r)
