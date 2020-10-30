1. clone the project repo and navigate to upwork-devs/moses-mugo

2. Run the command below to create and activate a virtual environment
  
  * '$python -m venv k8-venv'
  * '$source k8-venv/bin/activate' for Linux or 'cd k8-venv' and then 'Scripts\activate' and then 'cd .. ' for Windows
3. Run the command below to install dependencies
  * $pip install -r requirements.txt
4. Run '$cd notebooks' then run '$jupyter notebook' to view the notebooks

5. Run '$python main.py' to pull all the pull requests, issues and boards from all the repos saving them to /data as a csv files
