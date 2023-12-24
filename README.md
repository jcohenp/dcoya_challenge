# dcoya_assignment 

This repository contains various resources and configurations for managing a Kubernetes environment using Ansible, SSL certificates, Kubernetes configurations, testing scripts, and more.

## Prerequisites

- **Ansible Installed**: Ensure Ansible is installed on your local machine or control node.
- **Access to Kubernetes Environment**: Access to the Kubernetes cluster is required.
- **Python Environment**: Ensure Python 3.x is installed on the machine.
- **Git**: For cloning the repository and managing the source code.
- **Docker**: If working with Docker configurations.
- **Environment**: EC2 machine running on Ubuntu operating system


## Folder Structure:

- **Dockerfile**: used to build the image before to push to the docker registry.
- **index.html**: used by the dockerfile to set up the nginx page.
- **machine-name.txt**: used as environment file to let index.html file to display the machine name.
- **nginx.conf**: confiugration of our nginx with tls set up
- **ansible_kubernetes/**: Contains Ansible playbooks and roles for managing the Kubernetes environment.
  - **roles/**: Directory housing individual Ansible roles for specific configurations or tasks within the Kubernetes setup.
- **decoya-test/**: Folder for test scripts, ensuring the correct functioning of services deployed in the Kubernetes cluster.
- **README.md**: This document providing instructions, explanations, and a guide on how to use the repository.

## Actions Performed:

- **Dockerfile**:
    - The Dockerfile, would be used for defining the steps to create a Docker image encapsulating a specific application within the Kubernetes environment. It might detail the necessary dependencies, commands, and configurations required to build the image.
    - Generation of selfsigned certificate using openssl: (`subj "/C=IL/L=Tel aviv/O=JulOrganization/CN=dcoya"`)

- **Ansible Playbooks (`ansible_kubernetes/`)**:
  - Utilizes Ansible playbooks to automate Kubernetes environment setup, including installation, configuration, and management of services.
  - Installing Kubernetes main components: 
    - Kubectl: CLI used to communicate with the Kubernetes cluster
    - Kubelet: componenent that is facilitate the communication between control plane and normal nodes, execution of containarized app ...
    - Kubeadm: tool that is used to manage the cluster, init, update, maintenance...
  -  Creation of a new user that will be used to communicate with the kubernetes cluster
  -  Installing of google chrome: useful for running selenium (testing purpose)
  - Creation of a nginx deployment and Service using NodePort 30000 => accessible from outside using node IP and opened port. Nodeport should be used with caution because with default configuration it will have securit concerns. Use it only for testing/dev purpose or need to add configuration to secure it.

- **Testing Scripts (`decoya-test/`)**:
  - requierements.txt for setting up the test environment using pytest.
  - testing features:
    - The webpage is served correctly: Test if we can reach the nginx frontend and check if the title match the one defined in our index.html file.
    - A date is being: Test if the tag datetime and machinename exists and are not empty.
    - The date is correct: Get the date that exist within our dateime tag and compare it with the current date.
    - SSL correctness: Test if the self signed certificate that we are using exist and the differents fields that can be useful to validate the SSL communication.


### Configuration:

1. **Clone this repository:**

    ```
    git clone https://github.com/jcohenp/dcoya_challenge.git
    ```
2. **Build the Docker Image:**

    ```
    sudo docker build -t dcoya-nginx .
    ```
3. **Create a tag:**

    ```
    sudo docker tag <imageID> docker.io/jcohenp/dcoya
    ```
4. **Push the image in the Docker registry**

    ```
    sudo docker push docker.io/jcohenp/dcoya
    ```
2. **Update the `inventory` file with the IP address of your AWS EC2 instance:**

    ```ini
    [kubernetes-nodes]
    <your_instance_ip> ansible_user=ubuntu ansible_ssh_private_key_file=<path_to_ssh_key>
    ```

3. **Execute the initial setup playbook:**

    ```
    ansible-playbook -i inventory kubernetes_deploy.yml
    ```
4. **Connect to the new kubernetes user:**
    
    ```
    sudo su kubernetes
    ```
5. **Check if everything is setup on your kubernetes cluster:**
    
    **kubectl get nodes -o wide**
    ```
    NAME               STATUS   ROLES                  AGE    VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION   CONTAINER-RUNTIME
    ip-172-31-24-251   Ready    control-plane,master   113m   v1.21.1   172.31.24.251   <none>        Ubuntu 22.04.3 LTS   6.2.0-1017-aws   docker://24.0.7
    ```
    **kubectl get all -A**

    ```
    NAMESPACE     NAME                                           READY   STATUS    RESTARTS   AGE
    default       pod/nginx-deployment-d4cb4bf77-9xcq2           1/1     Running   0          112m
    default       pod/nginx-deployment-d4cb4bf77-pjlms           1/1     Running   0          112m
    kube-system   pod/calico-kube-controllers-7676785684-w89mk   1/1     Running   0          113m
    kube-system   pod/calico-node-nqx7j                          1/1     Running   0          113m
    kube-system   pod/coredns-558bd4d5db-l6tfs                   1/1     Running   0          113m
    kube-system   pod/coredns-558bd4d5db-mjmk9                   1/1     Running   0          113m
    kube-system   pod/etcd-ip-172-31-24-251                      1/1     Running   0          113m
    kube-system   pod/kube-apiserver-ip-172-31-24-251            1/1     Running   0          113m
    kube-system   pod/kube-controller-manager-ip-172-31-24-251   1/1     Running   0          113m
    kube-system   pod/kube-proxy-9zmhz                           1/1     Running   0          113m
    kube-system   pod/kube-scheduler-ip-172-31-24-251            1/1     Running   0          113m
    
    NAMESPACE     NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                  AGE
    default       service/dcoya-nginx   NodePort    10.98.123.246   <none>        443:30000/TCP            112m
    default       service/kubernetes    ClusterIP   10.96.0.1       <none>        443/TCP                  113m
    kube-system   service/kube-dns      ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP   113m
    
    NAMESPACE     NAME                         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
    kube-system   daemonset.apps/calico-node   1         1         1       1            1           kubernetes.io/os=linux   113m
    kube-system   daemonset.apps/kube-proxy    1         1         1       1            1           kubernetes.io/os=linux   113m
    
    NAMESPACE     NAME                                      READY   UP-TO-DATE   AVAILABLE   AGE
    default       deployment.apps/nginx-deployment          2/2     2            2           112m
    kube-system   deployment.apps/calico-kube-controllers   1/1     1            1           113m
    kube-system   deployment.apps/coredns                   2/2     2            2           113m
    
    NAMESPACE     NAME                                                 DESIRED   CURRENT   READY   AGE
    default       replicaset.apps/nginx-deployment-d4cb4bf77           2         2         2       112m
    kube-system   replicaset.apps/calico-kube-controllers-7676785684   1         1         1       113m
    kube-system   replicaset.apps/coredns-558bd4d5db                   2         2         2       113m
    ```
6. **Adding reference in the /etc/hosts of the node IP to avoid getting certificate invalid error due to self signed certificate**

    ```
    echo "<NODE_IP> <hostname>" 
    ```
    The hostname should match with the CN defined in the certificate

7. **Adding the self signed certificate in the list of CA in our system:**
    
    ```
    sudo docker cp <containerID>:/etc/ssl/certs/nginx-selfsigned.crt .
    sudo  cp nginx-selfsigned.crt /usr/local/share/ca-certificates/
    sudo update-ca-certificates
    ```
8. **Validate that the self signed certificate is working:**

    **curl -vv https://dcoya:30000**

    ```
    * Trying 100.26.40.113:30000...
    * Connected to dcoya (100.26.40.113) port 30000 (#0)
    * ALPN, offering h2
    * ALPN, offering http/1.1
    *  CAfile: /etc/ssl/certs/ca-certificates.crt
    *  CApath: /etc/ssl/certs
    * TLSv1.0 (OUT), TLS header, Certificate Status (22):
    * TLSv1.3 (OUT), TLS handshake, Client hello (1):
    * TLSv1.2 (IN), TLS header, Certificate Status (22):
    * TLSv1.3 (IN), TLS handshake, Server hello (2):
    * TLSv1.2 (IN), TLS header, Finished (20):
    * TLSv1.2 (IN), TLS header, Supplemental data (23):
    * TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
    * TLSv1.2 (IN), TLS header, Supplemental data (23):
    * TLSv1.3 (IN), TLS handshake, Certificate (11):
    * TLSv1.2 (IN), TLS header, Supplemental data (23):
    * TLSv1.3 (IN), TLS handshake, CERT verify (15):
    * TLSv1.2 (IN), TLS header, Supplemental data (23):
    * TLSv1.3 (IN), TLS handshake, Finished (20):
    * TLSv1.2 (OUT), TLS header, Finished (20):
    * TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
    * TLSv1.2 (OUT), TLS header, Supplemental data (23):
    * TLSv1.3 (OUT), TLS handshake, Finished (20):
    * SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
    * ALPN, server accepted to use http/1.1
    * Server certificate:
    *  subject: C=IL; L=Tel aviv; O=JulOrganization; CN=dcoya
    *  start date: Dec 22 13:26:06 2023 GMT
    *  expire date: Dec 21 13:26:06 2024 GMT
    *  common name: dcoya (matched)
    *  issuer: C=IL; L=Tel aviv; O=JulOrganization; CN=dcoya
    *  SSL certificate verify ok.
    * TLSv1.2 (OUT), TLS header, Supplemental data (23):
    > GET / HTTP/1.1
    > Host: dcoya:30000
    > User-Agent: curl/7.81.0
    > Accept: */*
    > 
    * TLSv1.2 (IN), TLS header, Supplemental data (23):
    * TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
    * TLSv1.2 (IN), TLS header, Supplemental data (23):
    * TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
    * old SSL session ID is stale, removing
    * TLSv1.2 (IN), TLS header, Supplemental data (23):
    * Mark bundle as not supporting multiuse
    < HTTP/1.1 200 OK
    < Server: nginx/1.24.0
    < Date: Sat, 23 Dec 2023 12:29:27 GMT
    < Content-Type: text/html
    < Content-Length: 1031
    < Last-Modified: Fri, 22 Dec 2023 13:25:16 GMT
    < Connection: keep-alive
    < ETag: "65858e3c-407"
    < Accept-Ranges: bytes
    < 
    <!DOCTYPE html>
    <html>
    <head>
      <title>Date and Machine Name</title>
      <script>
            document.addEventListener("DOMContentLoaded", function() {
                // Fetch machine name
                fetch('machine-name.txt')
                    .then(response => response.text())
                    .then(machineName => {
                        // Display machine name
                        document.getElementById("machinename").innerHTML = `Current Machine Name:   ${machineName.trim()}`;
    
                        // Get current date and time
                        var date = new Date().toLocaleString();
    
                        // Display current date and time
                        document.getElementById("datetime").innerHTML = `Current Local Date and Time: ${date}`;
                    })
                    .catch(error => {
                        console.error('Error fetching machine name:', error);
                    });
            });
        </script>
    </head>
    <body>
      <h1>Date and Machine Name</h1>
      <p id="datetime"></p>
      <p id="machinename"></p>
    </body>
    </html>
    * Connection #0 to host dcoya left intact
    ```

9. **Install all dependencies to run the python tests:**
    
    ```
    sudo python3 -m pip install -r requirements.txt
    ```
10. **Run python tests:**

    sudo pytest -v dcoya_tests/pytest_dcoya.py
    ```
    ===================================================================== test session starts =====================================================================
    platform linux -- Python 3.10.12, pytest-7.4.3, pluggy-1.3.0 -- /usr/bin/python3
    cachedir: .pytest_cache
    rootdir: /home/ubuntu/dcoya_challenge/dcoya_tests
    collected 4 items                                                                                                                                             
    
    pytest_dcoya.py::test_website_response_code PASSED                                                                                                      [ 25%]
    pytest_dcoya.py::test_machinename_and_datetime_exist PASSED                                                                                             [ 50%]
    pytest_dcoya.py::test_date_format PASSED                                                                                                                [ 75%]
    pytest_dcoya.py::test_ssl_certificate PASSED         
    ```
    
    ## Project Enhancement Plan
    
    ### Domain and Certificate
    - **Domain Creation**: Register a domain name to uniquely identify the project.
    - **Certificate Authority (CA)**: Obtain an SSL/TLS certificate from a trusted Certificate Authority instead of using self-signed certificates.
    
    ### Infrastructure Setup
    - **Service Type Load Balancer**: Implement a service type load balancer to distribute incoming traffic efficiently.
    - **Cloud Provider Integration**: Utilize the cloud provider's capabilities to manage traffic redirection to Nginx.
    
    ### Continuous Deployment
    - **Jenkins Pipeline**: Establish a continuous deployment pipeline in Jenkins to automate the deployment of new nodes.
    
    ### Kubernetes Cluster Setup
    - **Master and Worker Nodes**: Create a Kubernetes cluster architecture with dedicated master nodes for administrative tasks and worker nodes for application-related activities.
    - **Security Analysis**: Implement security measures for the Kubernetes cluster, including pods, to ensure robust protection against vulnerabilities and unauthorized access.
    
    ### Monitoring and Analysis
    - **Prometheus Integration**: Integrate Prometheus to monitor and check the status of the Kubernetes cluster, ensuring proactive identification of issues and performance analysis.
    
    ### Security Measures
    - **Web Application Firewall (WAF)**: Implement a WAF to control and manage incoming traffic, allowing filtering based on predefined rules to block potentially malicious IP addresses.
    
    ### Secrets Management
    - If any sensitive data is used (e.g., SSL certificates, API keys), demonstrate how to manage these securely within the deployment process.
    
    ### Automated Testing:
    - Introduce automated testing into the CI/CD pipeline to verify the functionality and performance of the deployed application automatically.
    
    ### Scalability and High Availability:
    - Address how the Kubernetes deployment can be scaled horizontally or made highly available, especially if this application is part of a production environment.

