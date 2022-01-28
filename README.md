# Reinforcement Learning Practical
# Final Project

#### Satchit Chatterji (S3889807)

This project acts as an extention for an earlier projects done for the Neural Networks course. The readme file below is still valid for this project, however, all associated files from that project are in the folder "NNProject". The remaining are the ones that are important for the RFL course:

> SARSAAgent.py

> trainSARSA.py

> episode.py

> flight_paths.py

> plot_scores.py

I hope you enjoy this project!

-----
# Neural Networks For AI
# Semester Project

#### Stefania Radu (s3919609)
#### Satchit Chatterji (s3889807)
#### Ruhi Mahadeshwar (s4014456)
#### Andreea Minculescu (s3932222)

## Abstract
Landing a spacecraft autonomously is a fundamental task in space exploration: it has to be precisely executed or it could lead to tremendous loss in terms of resources and human lives. As a result, computer precision has proved to be a strong candidate in solving the lunar landing task. In this present paper, we explore two different multilayer perceptron (MLP) architectures in a simplified 2-dimensional rocket control simulation with the final goal of landing the rocket as close as possible to a randomly generated target. The architectures have the same overall structure but differ in 1) the learning algorithm, one being evolutionary-based and the other using the error backpropagation method and 2) the kind of training, one being trained by playing games against itself and the other on human generated data. Although both architectures solve the lunar landing task, the evolutionary-based MLP is more robust in terms of the solution(s) found, while the backpropagation-based MLP reaches a good solution after a lower number of iterations.

## Instructions to play the simulation
Download or clone the repository to your machine, then run ``rocket_sim.py``. The first time it runs, it might need to download a Java-based library (Processing) which acts as a python backend.

The goal is to try and land the virtual rocket on the red pad.

Don't fall to hard or tilt too much though!


Use these keys to control the rocket:

	KEY   ->   BEHAVIOUR
  
	'w'   ->   Turn engine on
  
	' '   ->   Turn engine off <space>
  
	's'   ->   Stop rotation
  
	'a'   ->   Rotate anticlockwise (turn left)
  
	'd'   ->   Rotate anticlockwise (turn right)
  
	'r'   ->   Reset all values of rocket (pos, vel, acc)



You can play another game directly by pressing 'r'. Right after you land, the target is reset, so don't worry if it suddenly jumps away, your success/failure was duly recorded.

You can just close the pop up panel when you are done playing.

Thanks for playing!

Note: There is a very small chance that you could get an error that looks like this:

`The file "C:\Users\Satchit Chatterji\Desktop\FinalCodeVerssion\NeuralNetworksProject-main\RocketSimulation/rocket.png" is missing or inaccessible, make sure the URL is valid or that the file has been added to your sketch and is readable.`
Unfortunately the processing-py library used (https://github.com/FarukHammoud/processing_py) is limited and occasionally unstable for unclear reasons. Try redownloading or rebooting, it should fix the issue.

If not, this video is an example run: https://youtu.be/zxtcC-INAH0

## Questions/Feedback

Training, loading and running models should be fairly easy, but the code may not be the most transparent. Any questions or feedback can be sent to s.chatterji.1\[at\]student.rug.nl or as an issue in the github repo. 
