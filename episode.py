import numpy as np

def run_single_episode(scene, rocket, controller, agent, init, frames, continual_draw):

	if init is not None:
		scene.init_target(init)

	cur_frame = 0

	cumulative_score = 0
	while(True):

		cur_frame+=1
		if cur_frame>frames:
			print('Timeout!')
			rocket.is_dead = True


		# action = agent.get_decision(observation)
		# observation, reward, done, info = env.step(action)
		# agent.record_reward(reward, done)
		# cumulative_rewards[-1] += reward

		# agent.train_model()

		action = agent.get_decision(rocket.get_data_list())
		controller.control(action)
		rocket.update()
		reward = 500*np.exp(-((rocket.score(recalc=True)+50)**2)/(2)*0.007**2)

		agent.record_reward(reward, rocket.is_dead)
		cumulative_score += reward
		
		agent.train_model()

		if rocket.is_dead:
			# scene.draw()
			print("Rocket dead!")
			print(f"rocket target: {rocket.data['x_target']}")
			print(f"rocket final pos: {rocket.center_pos.x}, {rocket.center_pos.y}")

			return reward, cumulative_score

		if continual_draw:
			scene.draw()
