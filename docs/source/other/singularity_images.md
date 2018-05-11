# Singularity Images

Docker images will not run on aging1a and aging2a because of the outdated operating system. Craig Hamilton
figured out that he could convert the Docker images to a Singularity image so the BIDS Apps could run on  
these machines. How to convert the Docker Image to a Singularity image is detailed below.

Information about Docker can be found here https://www.docker.com/
Information about Singularity can be found here https://singularity.lbl.gov/


## Downloading a Docker Image

I am going to assume that you have Docker installed on our local machine. I have performed these instructions  
on my Mac Book Pro.

1. Run the Docker daemon
2. You have to pull the Docker image down. The docker images reside somewhere in the cloud and can be pulled  
   down with the command

```
docker pull <docker_image, bids/tracula>
```

A list of BIDS Apps can be found here https://github.com/BIDS-Apps.  Once you go to the link you can see a list  
of BIDS Apps that you can download.  When you look at the the individual BIDS Apps it helps to understand how Docker
runs a specific Docker Image.  Below is an example to run the BIDS App Tracula. You will see that there is a
command **docker run** followed by some optional parameters.

```
    docker run -ti --rm \
     -v /data/ds114/sourcedata:/bids_dataset:ro \
     -v /data/ds114/derivates/tracula:/outputs \
     -v /data/ds114/derivates/freesurfer:/freesurfer \
     bids/tracula \
     /bids_dataset /outputs participant --participant_label 01 \
     --license_key "XXXXXXXX" \
     --freesurfer_dir /freesurfer
 ```


After the -v parameters you will see the Docker Image

bids/tracula

This is the input you use to the docker pull command to download the Docker image to your local machine.


## Converting a Docker image to a Singularity container

These notes were provided by Craig Hamilton.

I used the instructions on converting fmriprep:
https://fmriprep.readthedocs.io/en/stable/installation.html#singularity-container

So, here is the command I ran on my Mac Book Pro to build a heudiconv
container:

```console
docker run --privileged -t --rm
  -v /var/run/docker.sock:/var/run/docker.sock 
  -v /tmp:/output 
  singularityware/docker2singularity bids/tracula:latest
```

It gets the docker container via the web from bids/tracula, evidently,
so don't need a copy of it locally. This put the singularity container
in my tmp directory, which I copied to /cenc/software/heudiconv. (the
/cenc mount was evidently not available to docker)

But, you can get a local copy if you want it:

* $ docker pull nipy/heudiconv
* $ docker pull poldracklab/fmriprep

(However, this local copy is put somewhere special, known to docker. It
doesn't go in the local directory. "docker images" will show your
images, but not where they reside.)

# Copy Singularity Image to desired Computer with Singularity Installed

I copied the files to aging1a using scp

scp bids_tracula_latest-2017-08-11-efd6196f92ca.img bkraft@aging1a.medeng.wfubmc.edu:/aging1/software/bids_apps


## Add Mounting points to Singularity image.

Once you have the Singularity image copied to the computer where you will be running your BIDS App you need
to mount the local directories to the Singularity container. You need root privileges on the computer where
you are installing the singularity container.

This allows the Singularity image to read data from your local machine and write its output to your local machine.

This requires you to run a root shell in the container and create the mount points. This command will give you a root shell inside the container.

```
sudo /usr/local/bin/singularity shell -w /aging1/software/bids_apps/bids_tracula_latest-2017-08-11-efd6196f92ca.img
```

then create the corresponding directories from your local machine in the Singularity container.

```
aging1a ➜  bids_apps sudo /usr/local/bin/singularity shell -w /aging1/software/bids_apps/bids_tracula_latest-2017-08-11-efd6196f92ca.img
Singularity: Invoking an interactive shell within container...

Singularity.bids_tracula_latest-2017-08-11-efd6196f92ca.img> # mkdir /cenc
Singularity.bids_tracula_latest-2017-08-11-efd6196f92ca.img> # mkdir /bkraft1
Singularity.bids_tracula_latest-2017-08-11-efd6196f92ca.img> # mkdir /gandg
Singularity.bids_tracula_latest-2017-08-11-efd6196f92ca.img> # exit
```