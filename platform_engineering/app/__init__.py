from CLI.ec2_manegment import *
from CLI.s3_manegment import *
from CLI.route53_manegment import *
## ec2
def action_ec2(request):
    if 'list' in request.args:
        return str(list_my_ec2())
    else:
        data = request.get_json()
                # Handle 'create' action
        if 'create' in request.args:
            return EC2(data.get('type'), data.get('image'))
                # Handle 'manage' action
        elif 'manage' in request.args:
            if data.get('status') == 'start':
                return start_ec2_instance(data['id'])
            elif data.get('status') == 'stop':
                return stop_ec2_instance(data['id'])
            # Return error if the action is not recognized
        else:
            return "THE action dont exists",400
    ## s3
def action_s3(request):
    if 'list' in request.args:
        return str(list_my_s3())
    else:
        data = request.get_json()
                # Handle 'create' action
        if 'create' in request.args:
            if data.get('security') == 'public' and data.get('sure') == 'yes':
                return create_s3(sure='yes')
            elif data.get('security') == 'private':
                return create_s3(sure='no')
            else:
                return "to create public bucket sure must be yes",400
        
        # Handle 'manage' action
        elif 'manage' in request.args:  # Should check query parameters
            if data.get('upload') and data.get('file_name'):
                return upload(data.get('upload'), data.get('file_name'))
            else:
                return "To upload a file, 'upload' and 'file_name' must be included", 400
        
        # Return error if the action is not recognized
        else:
            return "The action doesn't exist", 400
        ## route53
def action_route53(request):
    if 'list' in request.args:
        return str(list_hosted_zones_with_comment())
    else:
        data = request.get_json()
                # Handle 'create' action
        if 'create' in request.args:
            if data.get('security') == 'public':
                return create_zone(data.get('zone_name') or None, private=False)
            elif data.get('security') == 'private':
                return create_zone(data.get('zone_name') or None, private=True)
            else:
                return "to create zone security must be included",400
            
            # Handle 'manage' action
        
        elif 'manage' in request.args:
            if data.get('action') == 'update':
                # Check for required fields
                if not data.get('zone_name') or not data.get('record_name'):
                    return "zone_name and record_name must be included", 400
                if not data.get('ttl') and not data.get('values'):
                    return "ttl or values must be included", 400
                return create_dns_record( data['record_name'], data.get('type') or None, data.get('values') or None, data['action'], data['zone_name'], data.get('ttl') or None)
            elif data.get('action') == 'delete':
                        # Check for required fields

                if not data.get('zone_name') or not data.get('record_name'):
                    return "zone_name and record_name must be included", 400
                return create_dns_record( data['record_name'], data.get('type') or None, data.get('values') or None, data['action'], data['zone_name'], data.get('ttl') or None)
            else:
                        # Check for required fields to create a record

                if  not data['record_name'] or not data['type'] or not data['values'] or not data['action'] or not data['zone_name'] or not data['ttl']:
                    return "to create record 'record_name' 'type' 'values' 'action' 'zone_name' and 'ttl' must be included",400

                return create_dns_record( data['record_name'], data['type'], data['values'], data['action'], data['zone_name'], data['ttl'])
                
        else:
            # Return error if the action is not recognized
            return "The action doesn't exist", 400