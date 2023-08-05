import sys
import os
import json
import utils.helper as utils
import commons.config as config
import commons.constant as const

def login_ecs():
    login = utils.cmd_exec("aws ecr get-login   | sed  's/-e none//g'")
    utils.cmd_exec(login)


def get_last_task_definations(family_prefix):
    task_definations = utils.cmd_exec("aws ecs list-task-definitions --family-prefix " + family_prefix);
    return json.loads(task_definations)['taskDefinitionArns'][-1]


def get_task_defination_json(task_def_name):
    task_defination_json = utils.cmd_exec("aws ecs describe-task-definition --task-definition " + task_def_name);
    return json.loads(task_defination_json)


def update_task_image_version(task_def_json, version_number):
    imageName = task_def_json['taskDefinition']['containerDefinitions'][0]['image'];
    imageName = imageName.split(':')[0] + ':' + version_number
    task_def_json['taskDefinition']['containerDefinitions'][0]['image'] = imageName;
    print (json.dumps(task_def_json, indent=4))
    return task_def_json;


def cluster_list():
    clusters = utils.cmd_exec("aws ecs list-clusters")
    clusters = json.loads(clusters)
    return clusters['clusterArns']


def services_in_cluster(service_name):
    services = utils.cmd_exec("aws ecs list-services --cluster " + service_name)
    services = json.loads(services)
    return services['serviceArns']


def tasks_in_cluster(cluster_name, service_name):
    tasks = utils.cmd_exec("aws ecs list-tasks --cluster " + cluster_name + " --service-name " + service_name)
    tasks = json.loads(tasks)
    return tasks['taskArns']


def get_index_input(list, query):
    print("Select one " + query + " from the list: \n")
    index = 1
    for item in list:
        print(str(index) + ". " + item.split('/')[1])
        index = index + 1; 
    
    index = int(raw_input("\nYour Options? : "))
    print("Options? : " + query + " : " + list[index - 1]);
    return list[index - 1].split('/')[1]


def check_aws_cli():
    system_name = utils.get_system_type();
    path = const.ECS_CLI_PATH_MAP[system_name]
    
    print("system_name  : " + system_name + " \n Checking path : " + path)
    
    exists = os.path.isfile(path)
    
    if exists:
        print("ECS cli is Installed")
    else:
        print(const.ECS_CLI_INSTRUCTIONS)


def deploy():
    config.enable_debugging()
    check_aws_cli()
    # Keep presets
    clusters = cluster_list()
    cluser_name = get_index_input(clusters, "Cluster");
    
    services = services_in_cluster(cluser_name)
    service_name = get_index_input(services, "Service");
    
    tasks = tasks_in_cluster(cluser_name, service_name)
    
    task_name = get_index_input(tasks, "Task");
    
    utils.running_cmd("ecs-cli logs -c " + cluser_name + " --task-id " + task_name + " --follow")
    
    """
    image_version = "v_" + build_number
    task_family = "docker_ecs_app_image"
    last_task_def_name = get_last_task_definations(task_family)
    task_def_json = get_task_defination_json(last_task_def_name)
    task_def_json = update_task_image_version(task_def_json, image_version)
    print ('Last Updated Task definations : ' + json.dumps(task_def_json, indent=4))
    # Create a new task definition for this build
    # aws ecs register-task-definition --family docker_ecs_app_image --cli-input-json file://docker_boot_app-v_8.json
    utils.cmd_exec("aws ecs register-task-definition --family " + task_family + " --cli-input-json " + json.dumps(task_def_json) )    
    """

    
def find_ip():
    ec2_instances = utils.cmd_exec("aws ec2 describe-instances")
    ec2_instances = json.loads(ec2_instances)
    instanceToSearch = sys.argv[2];
    
    found_instance = {};
    print ("Searching the pattern : " + instanceToSearch)
    reservations = ec2_instances['Reservations'];
    for reservation in reservations:
        instances = reservation['Instances']
        for instance in instances:
            tags = instance['Tags'];
            # print("Tag : \n " + json.dumps(tags))
            for tag  in tags:
                tagKey = json.dumps(tag['Key']);
                tagValue = json.dumps(tag['Value']);
                if instanceToSearch in tagValue :
                    print("Value  : " + tagValue)
                    found_instance = instance;
                    break
    
    ip_address = found_instance['NetworkInterfaces'][0]['Association']['PublicIp'];
    print (ip_address)
