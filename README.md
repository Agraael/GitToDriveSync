# GitToDriveSync

GitToDrive is a python scrpit who allow to sync a git repository to a Google Drive Accout.  
It can be deployed inside a container , using the Dockerfile.

### Requirement

- **Python3**
- **[Drive](https://github.com/odeke-em/drive)**
- **Docker**


```
usage: GitToDriveSync.py [-h] {credential,init,start,auto} ...

Service who connect every update to a git branch into a Google drive

positional arguments:
  {credential,init,start,auto}
    credential          getting json credential for GoogleDrive
    init                init the drive directory and pull the repo
    start               start the GitToDrive" service/server on the directory
    auto                init and start the GitToDrive service/server

optional arguments:
  -h, --help            show this help message and exit
```