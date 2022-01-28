import os
import pandas as pd
import matplotlib.pyplot as plt

def is_reqd_game(lines, result):
	res_funcs = {'success' : lambda x: 'True' in x,
				 'failure' : lambda x: 'False' in x,
				 'all' : lambda x: True}
	return res_funcs[result](lines[0])

def extract_single_game_to_df(filename, result):
	lines = open(filename, 'r').readlines()
	if is_reqd_game(lines, result):
		lines.remove(lines[0])
		col_names = lines[0].strip().split(',')
		lines.remove(lines[0])
		split_lines = []
		for l in range(len(lines)):
			split_lines.append(lines[l].strip().split(','))
		df = pd.DataFrame(split_lines, columns=col_names)
		for col in col_names[:11]:
			if col=='engine':
				df[col] = df[col].astype(bool)
			else:
				df[col] = df[col].astype(float)
		return df

	return None

def get_games_as_lists(save_dir='saved_runs', result='success'):
	"""
	result:={'success', 'failure', 'all'}
	returns a dict of the form {file_name:[DataFrame(game_history)]}
	"""
	games = {}
	saved_games = [x for x in os.listdir(save_dir) if x.endswith('.csv')]
	for saved_game in saved_games:
		game_temp = extract_single_game_to_df(save_dir+'/'+saved_game, result)
		if game_temp is not None:
			games[saved_game] = game_temp
	return games

def plot_games(game_histories, center_targets = False):
	for game in game_histories.values():
		if center_targets:
			game['x_pos'] = game['x_pos'].add((game['x_target'].sub(500)).mul(-1))
		plt.plot(game['x_pos'].tolist(), [1000-x for x in game['y_pos'].tolist()], color='green')
	plt.show()

def plot_comparison(successes, failures, center_targets=False):
	# the i=0 thing and the if i==0 statements are just for the labels
	# and you can do without them, they don't matter
	i=0
	for game in failures.values():
		if center_targets:
			game['x_pos'] = game['x_pos'].add((game['x_target'].sub(500)).mul(-1))
		if i==0:
			plt.plot(game['x_pos'].tolist(), [1000-x for x in game['y_pos'].tolist()], color='gray', alpha=0.5, label='Failures')
		else:
			plt.plot(game['x_pos'].tolist(), [1000-x for x in game['y_pos'].tolist()], color='gray', alpha=0.5)
		i+=1

	i=0
	for game in successes.values():
		if center_targets:
			game['x_pos'] = game['x_pos'].add((game['x_target'].sub(500)).mul(-1))
		if i==0:
			plt.plot(game['x_pos'].tolist(), [1000-x for x in game['y_pos'].tolist()], color='green', label='Successes')
		else:
			plt.plot(game['x_pos'].tolist(), [1000-x for x in game['y_pos'].tolist()], color='green')
		i+=1

	plt.legend()
	plt.grid()
	plt.show()

def main():
	s = get_games_as_lists(result='success')
	f = get_games_as_lists(result='failure')
	# plot_games(s, False)
	plot_comparison(s, f, True)

main()
