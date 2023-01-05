# Development Setup

Assuming an AKS cluster already setup and registered in kubectl.

1. Install KubeRay Operator
2. Deploy a Ray cluster
	```bash
	kubectl apply -f deployment/ray-cluster.yml
	```
3. Port forward the managemend port of the cluster from one bash shell
	```bash
	kubectl port-forward service/graph-raycluster-autoscaler-head-svc 10001:10001
	```
4. Port forward the 8000 port from the cluster head pod from another bash shell

	Get name of pod for the cluster head service:
	```bash
	kubectl get pods
	```
	Example output:
	```bash
	NAME                                                   READY   STATUS    RESTARTS   AGE
	graph-raycluster-autoscaler-head-thr7w                 2/2     Running   0          27m
	graph-raycluster-autoscaler-worker-small-group-wjszz   1/1     Running   0          27m
	kuberay-operator-7fb4677468-gdvc7                      1/1     Running   0          3h58m
	```
	Setup port forwarding on the head pod:
	```bash
	kubectl port-forward pod/graph-raycluster-autoscaler-head-thr7w 8000:8000
	```

5. Every time you change your code and want to test it, just deploy it directly into the cluster. Run this from the code folder:
	See runtime-env.yml for the definition of the code location, ENV variables and pip packages dependencies.
	```bash
	serve run  --address=ray://127.0.0.1:10001 --runtime-env=runtime-env.yml graph:deployment_graph
	```

6. Test the Ray Serve deployments using a test client (or PostMan or curl)
	```bash
	python graph_client.py
	```