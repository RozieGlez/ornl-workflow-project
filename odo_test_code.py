import parsl
from parsl import python_app, bash_app
from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from parsl.providers import SlurmProvider
from parsl.launchers import SimpleLauncher
config = Config(
    executors=[
        HighThroughputExecutor(
            label="htex_Frontier",
            cores_per_worker=1,
            max_workers=1,
# Number of workers per node
            worker_debug=True,
            provider=SlurmProvider(
                partition="batch",
                account="trn025",

# Adjust this to
                nodes_per_block=1,
# Request one node
                init_blocks=1,
                min_blocks=1,
                max_blocks=1,
                launcher=SimpleLauncher(),
# Add any other SLURM options here
                worker_init='module load cray-python && source activate nodework',
# Add commands to set up your environment
                walltime='00:10:00',
# Set an appropriate walltime for your job
            ),
        )
    ],
    strategy=None,
)
@python_app
def hello_python (message):
    import time
    time.sleep(20)
    return 'Hello %s' % message
@python_app
def add_numbers ():
    total = 0
    with open("newfile.txt", 'r') as f:
        for line in f:
            total += int(line)
    return total


@bash_app
def hello_bash(message, stdout='hello-stdout'):
    return 'echo "Hello %s"' % message


parsl.load(config)
# invoke the Python app and print the result
# print(hello_python('World (Python)').result())
print(add_numbers().result())
