import requests, json

#1

def generate_response(payload, username, password, url_workflow):

        r = requests.post(
            url=url_workflow,
            auth=requests.auth.HTTPBasicAuth(
            username=username, password=password),
            data=payload,
            headers={'Content-Type':'application/json'}
            )

        response = r.json()
        return response


def toJSON(specs, username):
      pre_payload = {
                      "vm_name": specs['vm_name'],
                      "datastore_name": "vsanDatastore",
                      "vm_memory": specs['vm_memory'],
                      "vm_cpus": specs['vm_cpus'],
                      "disk_size": specs['vm_disk_size'],
                      "username": username,
                      "template": specs['template']
                    } 
      payload = { "extra_vars": pre_payload
                }
      payload = json.dumps(payload)
      return payload

class WorkflowManager:
    def __init__(self):
        self.username = "admin"
        self.password = "Admin1234!"

    def trigger_workflow_vm(self, values, username):
        """
    Lance le workflow de creation de VM
    """
        payload = toJSON(values, username)
        response = generate_response(payload, self.username, self.password, "http://192.168.10.5/api/v2/workflow_job_templates/15/launch/")
        print(response)
        return response
        
    def delete_vm(self, vm_name):

        """
    Lance le workflow de suppression de VM
    """
        payload = json.dumps({"extra_vars":{"vm_name": vm_name}})
        response = generate_response(payload, self.username, self.password, "http://192.168.10.5/api/v2/workflow_job_templates/19/launch/")
        print(response)
        return response

    def get_workflow_status(self, job_id):
        """
        récupère le status du workflow
        """
    
        r = requests.get( 
            url="http://192.168.10.5/api/v2/workflow_jobs/"+str(job_id)+"/",
            auth=requests.auth.HTTPBasicAuth(
            username=self.username, password=self.password),
            headers={'Content-Type':'application/json'}      
        )

        response = r.json()
        return response 
