# wandb gcp demo using terraform
Demo of terraform deployment of wandb platform on GCP

## Overview

The purpose of this demo is to show a basic deployment of Weights and Biases (W&B aka wandb) on GCP using using terrraform to deploy a kubernetes cluster. Referring to the [terraform module documentation here](https://github.com/wandb/terraform-google-wandb)

Please note that this setup is highly insecure and is not designed for production use of any kind.

There are 2 main sections of this README: 
 - Infrastructure deployment 
 - Example usage of the Weights and Biases (wandb)

 The end result of running this project is two main outcomes:
 - One, you will have deployed a kubernetes cluster that is running on google kubernetes engine, and that cluster will be scaled up to 2 replicas running wandb. You will expose a service that will allow you to connect to your W&B instance over the internet.
 - Two, you will be prepared to incorporate wandb libraries into your ML application and track your runs using the W&B UI.

## Infrastructure deployment

### Screenshots of example GCP deployment

Overview information
<img width="1126" alt="Screenshot 2024-04-08 at 8 30 03 PM" src="https://github.com/theodore-dream/wandb-terraform-demo/assets/20304946/3926e273-4620-4bd6-bd9d-b0964022a238">

Showing my kubernetes deployment has 2 replicas running
<img width="1134" alt="Screenshot 2024-04-08 at 8 32 14 PM" src="https://github.com/theodore-dream/wandb-terraform-demo/assets/20304946/9b3660bd-5311-46d1-aabe-6c0b5f6ed442">

Showing that my kubernetes service is running load balancer and exposing an accessible IP 
<img width="368" alt="Screenshot 2024-04-08 at 8 38 35 PM" src="https://github.com/theodore-dream/wandb-terraform-demo/assets/20304946/43abd570-ef57-4cad-afea-6d765e471ee0">


### Infrastructure Deployment

With this GCP terraform example, I want to provide complete step by step instructions to provide the steps I took to deploy this to an empty GCP project.

#### Prepare Your GCP Environment

- Create a GCP Project: If you haven’t already, create a new GCP project in the Google Cloud Console. This is where you will be deploying wandb. 
- Enable Billing: Make sure your project has billing enabled.
- Enable Necessary APIs: You need to enable the following APIs for your project:
    - Google Kubernetes Engine API
    - Google SQL Cloud API
    - Google Cloud Storage API
    - Google Pub/Sub API
    - Google Cloud DNS API

- Set Up Your Local Environment: Before you can deploy to the cloud, you'll want to setup your local environment, most likely your laptop
    - Install Terraform: Ensure you have Terraform installed on your local machine. It should be version 1 or above.
    - Install Google Cloud SDK: Install and initialize the Google Cloud SDK to interact with your GCP resources. Using the gcloud command can be helpful.

### Configure Terraform

Terraform is a highly advanced deployment tool which allows you to configure every part of your infrastructure. Each deployment is unique. The goal of this example is to allow you to deploy a very simple example deployment. 

 - Setup W&B terraform module:I have aleady incorporated the W&B terraform module into this repo. You can use this or clone that repo into your modules folder yourself. 
- Create Terraform Configuration: 
   - In the folder where you are running Terraform from, create/modify your own configuration file main.tf as shown using the provided main.tf file in this repo.
   - You will also need to specify your terraform.tfvars it should look something like this

```
project_id = "bionic-region-419521"
region     = "us-east1"
zone       = "us-east1-b"
namespace  = "theodore-unique"
license    = "<license>"
subdomain  = "wandb-sample"
domain_name = "theodore-demo.com"
```

 - Once you are ready to proceed, run `terraform init` to initialize your terraform project and then `terraform plan` to plan your deployment. This will show the changes that will be made on GCP. 
 - Once you are satisfied with your terraform deployment plan, run `terraform apply` to proceed with deployment
 - Review the output. The output of this terraform apply command will show you the URL to connect to your wandb deployment, however you cannot use this until you have finalized your deployment. 

### Review and finalize your environment

In this final step we scale up and we make sure we can access our cluster service endpoint over the internet. 

 - The following commands allow you to setup your CLI environment for gcloud CLI utility, allowing you to connect to your GCP GKE deployment of wandb. 

```
gcloud auth login
gcloud components install kubectl
gcloud config set project {YOUR_PROJECT_ID}
```

- Now you can get more information about your deployment:

```
gcloud container clusters list
gcloud container clusters get-credentials {CLUSTER NAME} --zone {ZONE}
kubectl get deployments
kubectl get services
```

- At this stage you may notice that the default deployment allows for up to 2 replicas, but by default will deploy 0 instances of wandb. You can run the following command to scale up to 2 replicas:

```
 kubectl scale deployment/wandb --replicas=2
```

 - There is another challenge to solve with the default deployment configuration. The gke_app specifies service type "Nodeport" which doesn't expose acess to the cluster. We want to change this to "LoadBalancer". Run the following commmand and  modify the config at bottom from `type: NodePort` to `type: LoadBalancer` 

```
kubectl edit svc wandb
```

 - You should now be able to see an external IP on the `wandb` service if you run `kubectl get services`

You can now access your wandb deployment by using the publicly exposed IP address and port from the above output and create your new account.

Once you have created your account in the UI you can use the following syntax to use the wandb CLI to double check your installation for any issues 

```
wandb login --relogin --host=<IP>:<PORT>
```

Now you can use the wandb CLI to help verify your installation using: `wandb status` and `wandb verify` 

## Example usage of the Weights and Biases

Weights & Biases is a machine learning platform for developers to build better models faster. In this example repo I am performing basic tests of model development on my M1 Macbook. 

I used an example project "my awesome project" to run different tests runs, or experiments, in the wandb platform. wandb provides me with additional observability and information about my runs so I can make more effective models. 

### Screenshots of wandb platform 

Here we can see some basic information about my organization to verify my setup.

<img width="1061" alt="Screenshot 2024-04-08 at 8 27 34 PM" src="https://github.com/theodore-dream/wandb-terraform-demo/assets/20304946/f3300c5e-f23c-4f8a-a0b4-bd1bfe5b222c">

Here we can see overview information about my runs.

<img width="1109" alt="Screenshot 2024-04-08 at 8 28 32 PM" src="https://github.com/theodore-dream/wandb-terraform-demo/assets/20304946/017ed400-a5b2-44fc-9ddc-37f9fcbfc050">

### wandb platform demo experimentation

Using the huggingface.py script, I am loading the "yelp_review_full" dataset and tokenizing this dataset with distilbert-base-uncased utility. I then significantly reduced the size of the dataset examples that are used, as well as reducing the size of the evaluation dataset.

From this base configuration, I then ran a set of 10 runs to test out the differences in different dataset examples, and dataset evaluation samples. I also iteratively modified batch sizes, and eval steps and max steps. Relevant code snippets shown here:  

```
# reduced the range of training examples to 300 to make it run faster
small_train_dataset = dataset["train"].shuffle(seed=42).select(range(300))

# reduced the range of evaluation samples to 50 to make it run faster
small_eval_dataset = dataset["test"].shuffle(seed=42).select(range(50))
```

Modifying the batch size

```
training_args = TrainingArguments(
    output_dir="models",
    report_to="wandb",
    logging_steps=5,
    per_device_train_batch_size=16,  # Reduced from 32 to 16
    per_device_eval_batch_size=16,  # Reduced from 32 to 16
    evaluation_strategy="steps",
    eval_steps=10,
    max_steps=50,
    save_steps=50,
)
```

Reviewing an overview of evaluation performance for the set of 10 runs that I completed, it is clear that overall, runs that included a larger number of steps led to higher evaluation accuracy.  

<img width="1338" alt="Screenshot 2024-04-08 at 9 04 56 PM" src="https://github.com/theodore-dream/wandb-terraform-demo/assets/20304946/ebee70e5-dce8-4aa0-ad23-0bf784739d5d">

The effect of batch sizes and minor tweaks on dataset examples and evaluation examples sizes is not immediately clear to me, however I can identify that some runs had significiantly improved performance over others in processing samples per second. 

Reviewing a comparison of train/loss I can observe that efficient_valley run had the least loss. Loss represents the poorness of a model's prediction strength, so we want to have low levels of loss.

<img width="1338" alt="Screenshot 2024-04-08 at 8 58 31 PM" src="https://github.com/theodore-dream/wandb-terraform-demo/assets/20304946/97e9c503-e556-44fe-b34c-a153bb03f9c7">

### wandb platform demo wrapup

It is clear that the wandb platform has comprehensive capabilities around model development and MLOPS workflows. For this demo, I focused on model creation, however in another future demo I hope to focus on model/LLM execution tracking and comparison features.
