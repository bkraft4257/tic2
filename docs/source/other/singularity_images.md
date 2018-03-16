# Singularity Images


## Downloading a Docker Image

1. Run the Docker daemon
1. docker pull nipy/heudiconv:latest

## Converting a Docker image to a Singularity container

These notes were provided by Craig Hamilton.

I used the instructions on converting fmriprep:
https://fmriprep.readthedocs.io/en/stable/installation.html#singularity-container

So, here is the command I ran on my Mac Book Pro to build a heudiconv
container:

```console
docker run --privileged -t --rm 
-v /var/run/docker.sock:/var/run/docker.sock 
-v /Users/crhamilt/tmp:/output
singularityware/docker2singularity nipy/heudiconv 
```

It gets the docker container via the web from nipy/neudiconv, evidently,
so don't need a copy of it locally. This put the singularity container
in my tmp directory, which I copied to /cenc/software/heudiconv. (the
/cenc mount was evidently not available to docker)

But, you can get a local copy if you want it:

* $ docker pull nipy/heudiconv
* $ docker pull poldracklab/fmriprep

(However, this local copy is put somewhere special, known to docker. It
doesn't go in the local directory. "docker images" will show your
images, but not where they reside.)


## Add Mounting points to Singularity image.