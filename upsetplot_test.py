from upsetplot import generate_counts
example_counts = generate_counts()
print(example_counts)

from upsetplot import UpSet
ax_dict = UpSet(example_counts).plot()