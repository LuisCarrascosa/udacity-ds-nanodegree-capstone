import math


class TriangularSchedule():
    def __init__(self, min_lr, max_lr, cycle_length, inc_fraction=None):
        self.min_lr = min_lr
        self.max_lr = max_lr
        self.cycle_length = cycle_length
        self.inc_fraction = inc_fraction

    def __call__(self, iteration):
        if iteration <= self.cycle_length*self.inc_fraction:
            unit_cycle = iteration * 1 / \
                (self.cycle_length * self.inc_fraction)
        elif iteration <= self.cycle_length:
            unit_cycle = (self.cycle_length - iteration) * 1 / \
                (self.cycle_length * (1 - self.inc_fraction))
        else:
            unit_cycle = 0
        adjusted_cycle = (
            unit_cycle * (self.max_lr - self.min_lr)) + self.min_lr

        return adjusted_cycle


class CosineAnnealingSchedule():
    def __init__(self, min_lr, max_lr, cycle_length, inc_fraction=None):
        """
        min_lr: lower bound for learning rate (float)
        max_lr: upper bound for learning rate (float)
        cycle_length: iterations between start and finish (int)
        """
        self.min_lr = min_lr
        self.max_lr = max_lr
        self.cycle_length = cycle_length

    def __call__(self, iteration):
        if iteration <= self.cycle_length:
            unit_cycle = (
                1 + math.cos(iteration * math.pi / self.cycle_length)) / 2
            adjusted_cycle = (
                unit_cycle * (self.max_lr - self.min_lr)) + self.min_lr
            return adjusted_cycle
        else:
            return self.min_lr


class CyclicalSchedule():
    def __init__(
        self, schedule_class, cycle_length, cycle_length_decay=1,
        cycle_magnitude_decay=1, **kwargs
    ):
        self.schedule_class = schedule_class
        self.length = cycle_length
        self.length_decay = cycle_length_decay
        self.magnitude_decay = cycle_magnitude_decay
        self.kwargs = kwargs

    def __call__(self, iteration):
        cycle_idx = 0
        cycle_length = self.length
        idx = self.length

        while idx <= iteration:
            cycle_length = math.ceil(cycle_length * self.length_decay)
            cycle_idx += 1
            idx += cycle_length

        cycle_offset = iteration - idx + cycle_length

        schedule = self.schedule_class(
            cycle_length=cycle_length, **self.kwargs
        )

        return schedule(cycle_offset) * self.magnitude_decay**cycle_idx


default_params = {
    "min_lr": 1,
    "max_lr": 2,
    "num_cycles": 1,
    "iterations": 500,
    "inc_fraction": 0.5,
    "cycle_length_decay": 1,
    "cycle_magnitude_decay": 1
}

learning_rate_functions = {
    "triangular": {
        "name": "Triangular",
        "function": TriangularSchedule,
        "params": {
            "min_lr": "Minimun learning rate",
            "max_lr": "Maximun learning rate",
            "num_cycles": "Number of cycles",
            "iterations": "Iterations (epochs)",
            "inc_fraction": "Increasing fraction",
            "cycle_length_decay": "Cycle length decay (1 no decay)",
            "cycle_magnitude_decay": "Cycle magnitude decay (1 no decay)"
        }
    },
    "cosineAnnealing": {
        "name": "Cosine Annealing",
        "function": CosineAnnealingSchedule,
        "params": {
            "min_lr": "Minimun learning rate",
            "max_lr": "Maximun learning rate",
            "num_cycles": "Number of cycles",
            "iterations": "Iterations",
            "cycle_length_decay": "Cycle length decay (1 no decay)",
            "cycle_magnitude_decay": "Cycle magnitude decay (1 no decay)"
        }
    }
}

# iterations = 500
# num_cycles = 3
