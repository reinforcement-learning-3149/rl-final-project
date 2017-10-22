import gym
import numpy as np
from gym.envs.classic_control import rendering

import sys
import tty
import select
import termios
from time import sleep

def user_input():	
	"""
	Description: Function to get userinput
	"""
	sleep(.001)
	if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
		ch = sys.stdin.read(1)
		return ch
	else:
		return None

def array_upsample(rgb_array, up_ratio =1):
	"""
	Description: This is a function helps to upsample origin rendering results provided by 'julian-ramos'
		on git hub. Reference: https://github.com/openai/gym/issues/550
	Params: 
		- rgb_array: Input origin render result
		- k: Upsample Ration
		- l: Upsample Ratio
	Return:
		- the upsampled display array
	"""
	if up_ratio <= 0: 
		print "Number of up_ration must be larger than one, returning default array!"
		return rgb_array	
	return np.repeat(np.repeat(rgb_array, up_ratio, axis=0), up_ratio, axis=1)

KEY_CONTROL_MAP = {
	'w' : 1,
	'a' : 3,
	'd' : 2,
	's' : 4,
	'j' : 5,
	'k' : 6,
	'l' : 7,
	'1' : 1,
	'2' : 2,
	'3' : 3,
	'4' : 4,
	'5' : 5,
	'6' : 6,
	'7' : 7,
	'8' : 8,
	'9' : 9,
	'0' : 10,
	'p' : 11,
 	'[' : 12,
	']' : 13
}


if __name__ == "__main__":
	viewer = rendering.SimpleImageViewer()
	env = gym.make("KungFuMaster-ram-v0")
	print("# Action Space #")
	print(env.action_space)
	print("# Observation Space #")
	print(env.observation_space)

	old_settings = termios.tcgetattr(sys.stdin)
	tty.setcbreak(sys.stdin.fileno())
	env.reset()


	action = env.action_space.sample()
	while True:
		ori = env.render("rgb_array")
		ups = array_upsample(ori,6)
		viewer.imshow(ups)

		uin = user_input()
		if (uin):
			print(uin)
			if uin == 'x':
				break
			if uin in KEY_CONTROL_MAP:
				action = KEY_CONTROL_MAP[uin]
			else:
				print "Warning: No such key match!"
		else:
			action = KEY_CONTROL_MAP['a']
			

		action = env.action_space.sample()	
		print action
		observation, reward, done, info = env.step(action)
		print "Curr Observation:",observation
		if done:
			print("Episode finished !")
			break

	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
