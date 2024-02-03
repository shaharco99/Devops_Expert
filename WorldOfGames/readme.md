# world of games
in this project you can play Currency Roulette Game, Guess game and Memory game.
you can do it by running this commends:

enter the root dir
```bash
$ cd WorldOfGames
```
for creating the docker container
```bash
$ docker-compose up -d
```
and copy the input URL to your browser 
To start playing score run 
```bash
$ docker exec -it score_flask python MainGame.py
```


### HELM FOR JENKINS
```bash
$ helm install jenkins jenkins/jenkins -f values.yaml --namespace=jenkins
```
After build crate a pipline and connect it to this git repo,
and run the jenkinsfile attached to build run and check the score_flask image 