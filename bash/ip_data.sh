read -p "Enter the Instance name: " instance
region=eu-west-2

# check how many instances are running with that name
instance_count=$(aws ec2 describe-instances --region $region --filters "Name=tag:Name,Values=*$instance*" --query "Reservations[*].Instances[*].InstanceId" --output text | wc -l)
echo "There are $instance_count instances with the name $instance"

# for each instance gather the instance id and public ip address if it exists and the name tag
for i in $(aws ec2 describe-instances --region $region --filters "Name=tag:Name,Values=*$instance*" --query "Reservations[*].Instances[*].InstanceId" --output text); do
    echo "Instance ID: $i"
    ip=$(aws ec2 describe-instances --region $region --instance-ids $i --query "Reservations[*].Instances[*].PublicIpAddress" --output text)
    echo "Public IP: $ip"
    name=$(aws ec2 describe-instances --region $region --instance-ids $i --query "Reservations[*].Instances[*].Tags[?Key=='Name'].Value" --output text)
    echo "Name: $name"
    echo "-------------------------"
done