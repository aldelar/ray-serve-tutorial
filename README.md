# Development Setup

Assuming an AKS cluster already setup and registered in kubectl.

1. Install KubeRay Operator
2. Deploy a Ray cluster
	```bash
	kubectl apply -f deployment/dev/ray-cluster.yml
	```

# Forwarding ports to localhost

1. Port forward the managemend port of the cluster from one bash shell
	```bash
	kubectl port-forward service/graph-raycluster-autoscaler-dev-head-svc 10001:10001
	```
2. Port forward the 8000 port from the cluster head pod from another bash shell

	Get name of pod for the cluster head service:
	```bash
	kubectl get pods
	```
	Example output:
	```bash
	NAME                                                      READY   STATUS    RESTARTS   AGE
	graph-raycluster-autoscaler-dev-head-m9rdn                2/2     Running   0          45s
	kuberay-operator-7fb4677468-gdvc7                         1/1     Running   0          25h
	raph-raycluster-autoscaler-dev-worker-small-group-qzsxk   1/1     Running   0          45s
	```
	Setup port forwarding on the head pod:
	```bash
	kubectl port-forward pod/graph-raycluster-autoscaler-dev-head-m9rdn 8000:8000
	```

# Pushing and testing your code

1. Every time you change your code and want to test it, just deploy it directly into the cluster. Run this from the code folder:

	If your code is running already in a terminal, Ctrl+C to kill it, then deploy:

	See runtime-env.yml for the definition of the code location, ENV variables and pip packages dependencies.
	From the 'service' folder, in a bash shell:
	```bash
	serve run --address=ray://127.0.0.1:10001 --runtime-env=../deployment/dev/runtime-env.yml graph:deployment_graph
	```

2. Test the Ray Serve deployments using a test client (or PostMan or curl)
	
	From the root folder, in a different bash shell:
	```bash
	python test/graph_client.py
	```

3. When done or need to deploy a change, Ctrl+C into the terminal running the 'serve run' command.

# Production deployment

1. Zip up the 'service' folder as service.zip and place it into deployment/prod folder

2. Deploy the Ray Serve service

	From the root folder of this project:
	```bash
	kubectl apply -f deployment/prod/ray-service.yml
	```