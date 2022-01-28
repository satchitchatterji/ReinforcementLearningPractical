import matplotlib.pyplot as plt
import numpy as np
import sys

def save_plots(file_ref):
	draw_type = 'mean'

	f = open(f'tests/{draw_type}_scores_{file_ref}.txt', 'r').readlines()[0].strip()
	f = f.replace('[', "")
	f = f.replace(']', "")
	vals = np.array([float(x) for x in f.split(',')])

	plt.plot(vals, color = 'red', label = draw_type)

	draw_type = 'min'
	f = open(f'tests/{draw_type}_scores_{file_ref}.txt', 'r').readlines()[0].strip()
	f = f.replace('[', "")
	f = f.replace(']', "")
	vals = np.array([float(x) for x in f.split(',')])

	plt.plot(vals, color = 'green', label = draw_type)

	plt.legend()
	plt.title(file_ref)
	plt.xlabel('Generation')
	plt.ylabel('Score')


	plt.savefig(f'test_imgs/{file_ref}_{draw_type}.png')

if __name__ == '__main__':
	if len(sys.argv) == 2:
		save_plots(sys.argv[1])
