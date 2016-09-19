from ipykernel.kernelapp import IPKernelApp
from .kernel import Sqlite3Kernel
IPKernelApp.launch_instance(kernel_class=Sqlite3Kernel)
