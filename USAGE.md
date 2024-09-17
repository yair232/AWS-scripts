## Usage Instructions

### CLI Usage

The CLI tool allows you to manage AWS resources (EC2, S3, Route 53) via simple commands. Below are examples of how to use the tool for different resources.

#### Available Commands

- **EC2 Instances**:
  - **Create EC2 Instance**:
    ```bash
    python main.py --resource ec2 --action create --instance_type t2.nano/t4g.nano --ami ubuntu/amazon
    ```
  - **List EC2 Instances**:
    ```bash
    python main.py --resource ec2 --action list
    ```
  - **Manage EC2 Instances**:
    - **Start EC2 Instance**:
      ```bash
      python main.py --resource ec2 --action manage --status start/stop --instance i-0abcdef1234567890/ all
      ```
- **S3 Buckets**:

  - **Create S3 Bucket**:
    ```bash
    python main.py --resource s3 --action create --security private/public
    ```
  - **Upload File to S3**:
    ```bash
    python main.py --resource s3 --action manage --file folder/myfile.txt --name myfile.txt
    ```
  - **List S3 Buckets**:
    ```bash
    python main.py --resource s3 --action list
    ```

- **Route 53 DNS**:

  - **Create DNS Zone**:

    ```bash
    python main.py --resource route53 --action create --zone_name example.com --security public/private
    ```

  - **Manage DNS Records**:
    - **Create DNS Record**:
      ```bash
      python main.py --resource route53 --action manage --function create --zone_name example.com --name www.example.com --type A --values 192.168.1.1 --ttl 'int'
      ```
    - **Update DNS Record**:
      ```bash
       python main.py --resource route53 --action manage --function update must -(zone_name,name)
       --ttl/values/type - at least one for change
      ```
    - **Delete DNS Record**:
      ```bash
      python main.py --resource route53 --action manage --zone_name example.com --name www.example.com
      ```
    - **List DNS Records**:
      ```bash
      python main.py --resource route53 --action list
      ```

#### Additional Arguments

- `--resource`: The AWS resource to manage (ec2, s3, route53)
- `--action`: Action to perform (create, list, upload, start, stop, create_record, update_record, delete_record, list_records, etc.)

### API Usage

The API provides programmatic access to the same AWS resource management functionalities as the CLI.

#### Available Endpoints

- **EC2 Management**:

  - **Create EC2 Instance**:  
    `POST /ec2`

    ```json
    {
      "instance_type": "t2.nano/t4g.nano", // Example: "t2.nano"
      "ami": "ubuntu/amazon" // Example: "ubuntu"
    }
    ```

  - **List EC2 Instances**:  
    `GET /ec2`

  - **Manage EC2 Instances**:

    - **Start/Stop EC2 Instance**:  
      `POST /ec2/manage`

      ```json
      {
        "status": "start/stop", // Example: "stop"
        "instance_id": "i-0abcdef1234567890", // Example: "i-0abcdef1234567890" or "all"
        "action": "stop" // Example: "stop"
      }
      ```

- **S3 Bucket Management**:

  - **Create S3 Bucket**:  
    `POST /s3`

    ```json
    {
      "bucket_name": "mybucket", // Example: "mybucket"
      "access": "private/public" // Example: "public"
    }
    ```

  - **Upload File to S3**:  
    `POST /s3/upload`

    ```json
    {
      "file": "C:\\Users\\Yair\\Desktop\\nitzanim\\AWS-scripts\\platform_engineering\\main.py", // Example: "path/to/file"
      "object_name": "nitzanim" // Example: "myfile.txt"
    }
    ```

  - **List S3 Buckets**:  
    `GET /s3`

- **Route 53 DNS Management**:

  - **Create DNS Zone**:  
    `POST /route53`

    ```json
    {
      "zone_name": "example.com", // Example: "yaircli232.com"
      "access": "private/public" // Example: "private"
    }
    ```

  - **Manage DNS Records**:

    - **Create DNS Record**:  
      `POST /route53/record/manage`

      ```json
      {
        "zone_name": "example.com", // Example: "example.com"
        "record_name": "www.example.com", // Example: "www.example.com"
        "record_type": "A", // Example: "A"
        "record_value": "192.168.1.1", // Example: "192.168.1.1"
        "ttl": 300 // Example: 300
      }
      ```

    - **Update DNS Record**:  
      `POST /route53/record/manage`

      ```json
      {
        "zone_name": "example.com", // Example: "example.com"
        "record_name": "www.example.com", // Example: "www.example.com"
        "ttl": 300, // Example: 300
        "record_value": "192.168.1.2", // Example: "192.168.1.2"
        "record_type": "A" // Example: "A"
      }
      ```

    - **Delete DNS Record**:  
      `POST /route53/record/manage`

      ```json
      {
        "zone_name": "example.com", // Example: "example.com"
        "record_name": "www.example.com", // Example: "www.example.com"
        "action": "delete" // Example: "delete"
      }
      ```

    - **List DNS Records**:  
      `GET /route53/records`

      ```json
      {
        "zone_name": "example.com" // Example: "example.com"
      }
      ```

#### Example API Requests

Here are some examples of how to use the API with `Invoke-RestMethod`:

- **Create DNS Zone**:

  ```powershell
  Invoke-RestMethod -Uri "http://127.0.0.1:2310/route53?create" -Method Post -Body '{"zone_name":"yaircli232.com","security":"private"}' -ContentType 'application/json'
  ```