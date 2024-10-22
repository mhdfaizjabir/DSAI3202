from mpi4py import MPI
from getmac import get_mac_address as gma

def get_mac_address():
	mac_address= gma()
	return   mac_address

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
	data = {'a': 7, 'b': 3.14}
	comm.send(data, dest=1, tag=11)
	print("The mac address of machine is", get_mac_address()) 
elif rank == 1:
	data = comm.recv(source=0, tag=11)
	print('On process 1, data received:', data)
	print("The mac address of machine is", get_mac_address())

