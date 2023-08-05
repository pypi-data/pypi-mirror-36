# Orchestrate
## Installation
Install [docker](https://www.docker.com/).

Build the base docker images by following the [README](docker/).

```bash
git clone git@github.com:sigopt/orchestrate.git
cd orchestrate
pip install .
sigopt test
```

## Help

To get the most up-to-date information about available commands, run
```bash
sigopt -h
```

Similarly, for usage about a particular command, run
```bash
sigopt logs -h
```

## Manage kubernetes clusters

### Create a cluster

```bash
sigopt cluster create -f examples/clusters/hybrid_cluster.yml
```

*Note: Creating a cluster with GPU support requires that you accept the
end user license agreement (EULA) for the EKS-optimized AMI with GPU support.
This can be done [here](https://aws.amazon.com/marketplace/pp/B07GRHFXGM)
by subscribing to the AMI.*

### Destroy a cluster

```bash
sigopt cluster destroy --cluster-name orchestrate
```

## Run Example Experiment

```bash
cd orchestrate/examples/sgd_classifier
sigopt run
```

Example running Orchestrate from a different directory:
```bash
cd orchestrate
sigopt run --directory examples/sgd_classifier/ -f examples/sgd_classifier/orchestrate.yml
```

## Connect to someone else's cluster
Every cluster creates an access role, `<cluster_name>-k8s-access-role`.

If you created the cluster, you already have access to role. To grant team member permission to access the cluster, use the [AWS IAM console](https://console.aws.amazon.com/iam/home#/roles) to add their IAM User as a "trusted entity" to access this role.

Once a user has the correct permission to assume the IAM role they can configure orchestrate to use your cluster:

```
sigopt cluster connect --cluster-name <cluster name>
```

## Installation for Development
Install [docker](https://www.docker.com/).

Clone the repo:
```bash
git clone git@github.com:sigopt/orchestrate.git
cd orchestrate
```

Create a virtual environment:
```
pip install virtualenv
cd sigopt-api
virtualenv -p `which python3.6` venv
```

Activate the virtual environment:
```
source venv/3.6/bin/activate
```

Install development and production dependencies:
```
make update
```

### Option #1: install the orchestrate package locally
Install the orchestrate cli and python package into your local virtualenv. Please note that changes you make while you are developing will require you to re-install the package to see the changes reflected:

```
pip install .
```

Now you can run commands as above, like

```
sigopt -h
```
### Option #2: run orchestrate directly

Invoke the orchestrate CLI directly, without installing package, by using the bin script from this repository:
```
./bin/sigopt -h
```

## Debugging

### Run kubectl on your cluster

```bash
sigopt kubectl get nodes
```

Read the documentation for [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/).

## License

Licensed under [Apache 2.0](LICENSE.md).
