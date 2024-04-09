# wandb-gcp-demo
demo of terraform deployment of wandb platform 

## Overview

The purpose of this demo is to show a basic deployment of Weights and Biases (W&B aka wandb) on GCP using using terrraform to deploy a kubernetes cluster. Referring to the [terraform module documentation here](https://github.com/wandb/terraform-google-wandb)

There are 2 main sections of this README: 
 - Infrastructure deployment 
 - Example usage of the Weights and Biases (wandb)

 The end result of running this project is two main outcomes:
 - One, you will have deployed a kubernetes cluster that is running on google kubernetes engine, and that cluster will be scaled up to 2 replicas running wandb. You will expose a service that will allow you to connect to your W&B instance over the internet.
 - Two, you will be prepared to incorporate wandb libraries into your ML application and track your runs using the W&B UI.

### Infrastructure Deployment

With this GCP terraform example, I want to provide complete step by step instructions to provide the steps I took to deploy this to an empty GCP project.

#### Prepare Your GCP Environment**

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