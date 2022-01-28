import matplotlib.pyplot as plt

def plot_scores(last_scores, cum_scores, filename):
	""" Plot the scores of a learning agent. Note that these are NOT print-ready
		and should only be used for debugging or testing purposes. """
	avg = lambda x: sum(x)/len(x)

	plt.plot(last_scores, label="Terminal reward")
	plt.plot([avg(last_scores[:i]) for i in range(1,len(last_scores))], label="Cumulative average")
	plt.plot(range(20,len(last_scores)), [avg(last_scores[i:i+20]) for i in range(len(last_scores)-20)], label="Moving average (20)")
	plt.grid(True)
	plt.legend()
	plt.savefig(filename+"_terminal.png")
	plt.clf()

	plt.plot(cum_scores, label="Cumulative reward")
	plt.plot([avg(cum_scores[:i]) for i in range(1,len(cum_scores))], label="Cumulative average")
	plt.plot(range(20,len(cum_scores)), [avg(cum_scores[i:i+20]) for i in range(len(cum_scores)-20)], label="Moving average (20)")
	plt.grid(True)
	plt.legend()
	plt.savefig(filename+"_cumulative.png")
	plt.clf()