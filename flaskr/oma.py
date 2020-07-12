import math
from matplotlib.figure import Figure


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
    def __init__(self, min_lr, max_lr, cycle_length):
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


# self, schedule_class, cycle_length, cycle_length_decay=1, cycle_magnitude_decay=1
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


def draw(schedule, title, iterations=150):
    fig = Figure(figsize=(6, 4), dpi=200)
    axis = fig.add_subplot(1, 1, 1, label="hola")

    axis.plot(
        [i+1 for i in range(iterations)],
        [schedule(i) for i in range(iterations)]
    )

    axis.grid(True)
    axis.autoscale_view()
    axis.set_title("(Triangular) Learning rate for each epoch")
    axis.set_xlabel("Epoch")
    axis.set_ylabel("Learning Rate")

    fig.savefig(title, format="png")


iterations = 500
num_cycles = 3

# TriangularSchedule(min_lr=1, max_lr=2, cycle_length=1000, inc_fraction=0.2)
schedule = CyclicalSchedule(
    TriangularSchedule,
    min_lr=1,
    max_lr=2,
    cycle_length=int(iterations/num_cycles),
    cycle_length_decay=0.8,
    cycle_magnitude_decay=0.8,
    inc_fraction=0.2
)

draw(schedule, 'learning_TriangularSchedule', iterations)

# CosineAnnealingSchedule(min_lr=1, max_lr=2, cycle_length=1000)
schedule1 = CyclicalSchedule(
    CosineAnnealingSchedule,
    min_lr=1,
    max_lr=2,
    cycle_length=int(iterations/num_cycles),
    cycle_length_decay=0.8,
    cycle_magnitude_decay=0.8
)

draw(schedule1, 'learning_CosineAnnealingSchedule', iterations)
