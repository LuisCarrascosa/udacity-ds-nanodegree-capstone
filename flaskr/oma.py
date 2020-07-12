import learning_rate as learning_rate
import painter as painter


iterations = 500
num_cycles = 1
# TriangularSchedule(min_lr=1, max_lr=2, cycle_length=1000, inc_fraction=0.2)
schedule = learning_rate.CyclicalSchedule(
    learning_rate.TriangularSchedule,
    min_lr=1,
    max_lr=2,
    cycle_length=int(iterations/num_cycles),
    cycle_length_decay=0.8,
    cycle_magnitude_decay=0.8,
    inc_fraction=0.2
)

base64_graph = painter.draw_learning_rate(
        schedule,
        "hola peo", iterations)

print(f"base64_graph: {base64_graph}")

# # CosineAnnealingSchedule(min_lr=1, max_lr=2, cycle_length=1000)
# schedule1 = CyclicalSchedule(
#     CosineAnnealingSchedule,
#     min_lr=1,
#     max_lr=2,
#     cycle_length=int(iterations/num_cycles),
#     cycle_length_decay=0.8,
#     cycle_magnitude_decay=0.8
# )

# draw(schedule1, 'learning_CosineAnnealingSchedule', iterations)
