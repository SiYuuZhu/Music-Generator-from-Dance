# Music-Generator-from-Dance


## Overview
For our capstone project, we developed a platform ***“Music-Generator-from-Dance”*** , which leverages machine learning to synthesize unique music through our instinctive body movements, without profound knowledge of music theory.


## Features
- *Intuition*  - no prior knowledge required, just dance at wil
- *Uniqueness* - Different movements produce different music
- *Convenience* - Significantly shorten the time to create a piece of music


## Architecture
![image (1)](https://github.com/user-attachments/assets/1ffae208-cb54-48ba-9a3c-c5f0a2055d92)
- Utilize OpenPose to extract the keypoints of the human skeleton from each frame
- Identify the dance style by Dynamic Time Warping(DTW)
- Use Magenta - interpolation mode to generate continuously smooth morphing between styles<br>
i.e., as the dance style changes, the music style seamlessly transitions as well    
- Modulate the tempo of generated music based on kinematic beat detector by Mido
- Build the web with Django framework

## Environment
set up a virtual environment to manage dependencies:
- Python 3.8.3
- Tensorflow 1.14.0
- Openpose 1.7.0
- Magenta 2.1.3
- DTW(dtaidistance) 2.0
- Mido 1.2.6
- Django 3.2.3


## Demo
### [Demo: Generated Music with origin dance video](https://www.youtube.com/watch?v=kNr6kWlKy0k)
https://github.com/user-attachments/assets/b763dd4b-c925-4173-9d53-5f587dfe5835

### Demo: Web
![music-generator-from-dance](https://github.com/user-attachments/assets/d80b8985-255b-41c1-b97e-70531bf10168)
