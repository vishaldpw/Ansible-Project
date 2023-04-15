import paramiko
import jinja2
import os

# Define target servers
targets = ['target1', 'target2']
# Define SSH credentials
username = 'your_username'
password = 'your_password'

# Create SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Dictionary to store server information
servers = []

# Iterate through target servers
for target in targets:
    try:
        # Connect to the target server
        client.connect(target, username=username, password=password)

        # Check if Ansible is installed
        stdin, stdout, stderr = client.exec_command('ansible --version')
        output = stdout.read().decode('utf-8')
        if 'ansible' in output:
            ansible_installed = True
        else:
            ansible_installed = False

        # Add server information to the dictionary
        server_info = {
            'server': target,
            'ansible_installed': ansible_installed
        }
        servers.append(server_info)

        # Close the SSH connection
        client.close()
    except paramiko.AuthenticationException:
        print(f'Authentication failed for {target}.')
    except paramiko.SSHException:
        print(f'Unable to establish SSH connection to {target}.')
    except paramiko.Exception as e:
        print(f'Error while connecting to {target}: {str(e)}')
    finally:
        client.close()

# Create HTML report using Jinja2 template
template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(os.path.abspath(__file__)))
template_env = jinja2.Environment(loader=template_loader)
template_file = 'template.html'  # Path to your template file
template = template_env.get_template(template_file)
html_output = template.render(servers=servers)

# Write HTML output to index.html file
with open('index.html', 'w') as f:
    f.write(html_output)

print('HTML report generated successfully as index.html')
