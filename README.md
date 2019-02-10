# JumpAwake
[XdHacks 2019] Do jumping jacks to silence your alarm!

## Development
### Deploy To Google Cloud Platform
```sh
# Initialize terraform once
terraform init

# Create resources for the demo
terraform apply

# Transfer production files to Google Cloud Compute instance
./frontend/create_build.sh
./sync.sh

# Clean up resources after demoing
terraform destroy
```