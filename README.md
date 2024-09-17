# Platform Engineering Automating AWS Resource Provisioning

## Overview

This project automates AWS resource provisioning using a Python-based CLI tool. It empowers developers to self-manage EC2 instances, S3 buckets, and Route 53 DNS records while adhering to DevOps standards. The project consists of three main phases:

- **Phase 1:** Core CLI Development
- **Phase 2:** Adding a UI in Jenkins
- **Phase 3:** Creating a RESTful API

## Phase 1: Core CLI Development

In this phase, I developed a Python CLI tool that allows developers to:

### EC2 Instances

- **Create:** Provision new EC2 instances with options for `t3.nano` or `t4g.nano` types, and limit to a maximum of two running instances.
- **AMI Choice:** Choose between the latest Ubuntu or Amazon Linux AMI.
- **Manage Instances:** Start and stop instances created through the CLI.
- **List Instances:** List all EC2 instances created via the CLI.

### S3 Buckets

- **Create:** Create new S3 buckets with options for public or private access.
- **Confirmation for Public Buckets:** Confirm public access with an additional approval step.
- **File Upload:** Upload files to buckets created through the CLI.
- **List Buckets:** List all S3 buckets created via the CLI.

### Route53 DNS Records

- **Create Zones:** Create DNS zones using Route53.
- **Manage DNS Records:** Create, update, or delete DNS records for zones created through the CLI.

## Phase 2: Adding a UI in Jenkins

In this phase, I integrated the Python CLI tool with Jenkins to provide a user-friendly UI. This phase includes:

- **Screens/Jobs:** Each resource is implemented as a different Jenkins job or screen.
- **Photos:** Visuals of the Jenkins UI are included to demonstrate the integration.
  ![Alt text](/platform_engineering/images/EC2.png)

![Alt text](/platform_engineering/images/S3.png)

![Alt text](/platform_engineering/images/Route53.png)

## Phase 3: Creating a RESTful API

For advanced functionality, I wrapped the CLI tool with a RESTful API to enable programmatic interaction with the platform. This phase enhances scalability and flexibility by allowing developers and other tools to:

- **Interact Programmatically:** Perform resource management tasks via API calls.

### Docker Images

To simplify deployment, two Docker images are available:

#### 1. CLI Docker Image

This image contains the Python-based CLI tool for managing AWS resources.

- **Docker Hub URL:** `docker pull yair23/python-aws-cli:latest`

#### 2. API Docker Image

This image contains the RESTful API for interacting with the CLI tool programmatically.

- **Docker Hub URL:** `docker pull yair23/flask-aws-app:latest`

### Running the Docker Images

**To run the CLI Docker container:**

```bash
docker run -d -p 2310:2310 -v C:\Users\<YourUsername>\.aws\ yair23/flask-aws-app:latest
```

## Installation and Usage

- **Dependencies:** Ensure you have Python and the necessary libraries installed.

## Usage Instructions

For detailed usage instructions, including CLI commands and API endpoints, refer to the [Usage Documentation](USAGE.md).

