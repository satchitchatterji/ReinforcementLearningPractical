import numpy as np

def run_single_trial(scene, rockets, controllers, cns, init, frames, continual_draw):
	
	if init is not None:
		scene.init_target(init)

	cur_frame = 0
	scores = []

	while(True):

		cur_frame+=1
		if cur_frame>frames:
			print('Timeout!')
			for rocket in rockets:
				rocket.is_dead = True

		for i in range(len(rockets)):
			rocket = rockets[i]
			controller  = controllers[i]
			cn = cns[i]

			if rocket.is_dead:
				continue

			decision = cn.get_decision(rocket.get_data_list())

			controller.control(decision)
			rocket.update()

		deaths = sum([r.is_dead for r in rockets])
		if deaths == len(rockets):
			# scene.draw()
			
			print("All rockets dead!")
			scores = [r.score(recalc=True) for r in rockets]
			print(f"rocket target: {rockets[0].data['x_target']}")
			print(f"rocket final pos: {rockets[0].center_pos.x}, {rockets[0].center_pos.y}")
			print(f'Min trial score: {min(scores)}')
			return scores

		if continual_draw:
			scene.draw()


def run_multi_trials(n_trials, scene, rockets, controllers, cns, init=None, frames=60*20, continual_draw=False):
	scores = np.zeros(len(rockets))
	for _ in range(n_trials):
		cur_scores = run_single_trial(scene, rockets, controllers, cns, init, frames, continual_draw)
		scores = np.add(scores, np.array(cur_scores)/n_trials)
		for rocket in rockets:
			rocket.reset_all()
	return scores
	