read -p "Enter the Instance name: " instance
region=eu-west-2

# check how many instances are running with that name
instance_count=$(aws ec2 describe-instances --region $region --filters "Name=tag:Name,Values=*$instance*" --query "Reservations[*].Instances[*].InstanceId" --output text | wc -l)
echo "There are $instance_count instances with the name $instance"

for instance in $(echo "$instances" | jq -r '.Reservations[].Instances[] | .InstanceId + "," + .PublicIpAddress + "," + (.Tags[] | select(.Key=="Name").Value)'); do
    IFS=',' read -r id ip name <<< "$instance"
    echo "Instance ID: $id"
    echo "Public IP: $ip"
    echo "Name: $name"
    echo "-------------------------"
done
