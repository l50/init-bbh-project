# init-bbh-project

This project is used to create a workspace with the necessary tools I need for bug bounty hunting

## Dependencies
* [Docker](https://www.docker.com/)

## Installation
```
make build
```

## Create a project
```
./init-bbh-project -t <name of program> -p ~/bug_bounty_hunting/
```

## TODO
- [] Create a central generic tools folder if it doesn't exist; if it does exist, make sure all tools are there
- [] Clone seclists in this generic tools folder if it doesn't exist
- [] Throw this in tools https://gist.github.com/jhaddix/86a06c5dc309d08580a018c66354a056
- [] Add this: https://gist.github.com/jhaddix/b80ea67d85c13206125806f0828f4d10
