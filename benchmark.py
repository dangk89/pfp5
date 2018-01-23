
# coding: utf-8

# In[31]:


import glob
import subprocess
from io import TextIOWrapper


# In[56]:


degrees_file = "data/frmtodeg/degrees.txt"
runtimes_file = "data/runtimes.txt"


# In[43]:


def read_runtime(skip):
    with open(runtimes_file) as runtimes:
        for x in range(skip):
            runtimes.readline()
        return runtimes.readline()


# In[94]:


def benchmark(iteration, links_file, ranks_file):
    cmd = "cat {} {} {} | ./pr_naive -r 2 -t {}".format(links_file, degrees_file, ranks_file, runtimes_file)
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf8") as proc:
        output, errors = proc.communicate()
        return (read_runtime(1), output)


# In[107]:


def calculate_initial_ranks():
    with open(degrees_file) as degrees:
        pages = degrees.read().count(",") + 1
        return [str(1 / pages * 1000000) for _ in range(pages)]


# In[108]:


# Prepare the benchmark runtimes
runtimes = []

# Calculate the initial ranks
with open("data/initial_ranks.txt", "w") as initial_ranks_file:
    initial_ranks_file.write('[{}]'.format(','.join(calculate_initial_ranks())))


# In[ ]:

# Run the benchmark
for index, links_file in enumerate(glob.iglob("data/frmtodeg/link*.txt")):
    print("Running iteration {}".format(index))
    if index == 0:
        ranks_file = "data/initial_ranks.txt"
    else:
        ranks_file = "data/ranks{}.txt".format(index)
    (runtime, new_ranks) = benchmark(index, links_file, ranks_file)
    runtimes.append(runtime)
    with open("data/ranks{}.txt".format(index + 1), "w") as new_ranks_file:
        new_ranks_file.write(new_ranks)


# In[ ]:
import numpy as np
print(runtimes)
np_runtimes = np.array(list(map(int, runtimes)))
print(np_runtimes)
print(np_runtimes.sum())
