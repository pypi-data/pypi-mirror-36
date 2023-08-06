from __future__ import absolute_import, division, print_function
import sys
import inspect
import json
import traceback
from dill.source import getname
from terraform_model.validator import CloudformationValidator
from terraform_model.parser import TransformRegistry
from terraform_model.validator import ReferenceValidator
from terraform_model.model import CfnModel
from terraform_model.model import IAMManagedPolicy
from terraform_model.model import IAMRole
from terraform_model.model import IAMUser
from terraform_model.model import IAMGroup
from terraform_model.model import IAMPolicy
from terraform_model.model import EC2Instance
from terraform_model.model import EC2SecurityGroup
from terraform_model.model import EC2SecurityGroupEgress
from terraform_model.model import EC2SecurityGroupIngress
from terraform_model.model import ElasticLoadBalancingLoadBalancer
from terraform_model.model import ElasticLoadBalancingV2LoadBalancer
from terraform_model.model import S3BucketPolicy
from terraform_model.model import SNSTopicPolicy
from terraform_model.model import SQSQueuePolicy
from terraform_model.model import ModelElement
from terraform_model.model.Parameter import Parameter
from terraform_model.parser.ParserRegistry import ParserRegistry
from terraform_model.parser.SecurityGroupParser import SecurityGroupParser
from terraform_model.parser.Ec2NetworkInterfaceParser import Ec2NetworkInterfaceParser
from terraform_model.parser.Ec2InstanceParser import Ec2InstanceParser
from terraform_model.parser.LoadBalancerParser import LoadBalancerParser
from terraform_model.parser.LoadBalancerV2Parser import LoadBalancerV2Parser
from terraform_model.parser.IamGroupParser import IamGroupParser
from terraform_model.parser.IamUserParser import IamUserParser
from terraform_model.parser.IamRoleParser import IamRoleParser
from terraform_model.parser.WithPolicyDocumentParser import WithPolicyDocumentParser
from terraform_model.model.Policy import Policy
from terraform_model.model.PolicyDocument import PolicyDocument
from terraform_model.parser.PolicyDocumentParser import PolicyDocumentParser
from terraform_model.parser.ParserError import ParserError


def lineno():
    """Returns the current line number in our program."""
    return str(' - CfnParser - line number: '+str(inspect.currentframe().f_back.f_lineno))


class CfnParser:
    """
    Cloudformation parser
    """
    def __init__(self, debug=False):
        """
        Initialize
        :param debug: 
        """
        self.debug = debug

        if self.debug:
            print('CfnParser - init'+lineno())


    # Given raw json/tf CloudFormation template, returns a CfnModel object
    # or raise ParserErrors if something is amiss with the format
    def parse(self,cloudformation_yml, parameter_values_json=None):

        if self.debug:
            print("\n\n#######################################################")
            print('CfnParser - parse')
            print('Beginning to parse cloudformation template')
            print('cloudformation type: '+str(type(cloudformation_yml)))
            print("##########################################################\n\n")
        try:
            self.pre_validate_model(cloudformation_yml)

            if self.debug:
                print('successful pre_validate_model: '+lineno())

        except ParserError as e:
            tb = sys.exc_info()[-1]
            if self.debug:
                print('tb: ' + str(tb) + lineno())
            stk = traceback.extract_tb(tb, 1)
            if self.debug:
                print('stk: ' + str(stk) + lineno())
            fname = stk[0][2]
            if self.debug:
                print('The failing function was', fname,lineno())
            raise

        if self.debug:
            print("\n\n#########################################")
            print('cloudformation template pre_validated'+lineno())
            print('Prevalidating cloudformation template')
            print("#############################################\n\n")


        # Transform raw resources in template as performed by
        # transforms
        transformer = TransformRegistry.TransformRegistry(debug=self.debug)
        cloudformation_yml = transformer.perform_transforms(cloudformation_yml)

        if self.debug:
            print("\n\n#################################################")
            print('Done prevalidating cloudformation template')
            print('cloudformation_yml type: '+str(type(cloudformation_yml))+lineno())
            print('Begin to validate referenses'+lineno())
            print("#####################################################\n\n")


        # Not validating references, because I believe terraform will do this internally
        #self.validate_references(cloudformation_yml)


        if self.debug:
            print("\n\n##########################################")
            print('Begin transform_hash_into_model elements')
            print('Creating the cfn_model objects')
            print("#############################################\n")

        cfn_model = CfnModel.CfnModel(debug=self.debug)
        cfn_model.raw_model=cloudformation_yml

        # pass 1: wire properties into ModelElement objects
        cfn_model = self.transform_hash_into_model_elements(cloudformation_yml, cfn_model)


        if self.debug:
            print("\n\n#################################################")
            print("Iterate through each resource in the model")
            print("######################################################\n")

            for r in cfn_model.resources:
                print("############### RESOURCE INFO ###################")
                print(r)
                print('resource_type: '+str(cfn_model.resources[r].resource_type)+lineno())
                print('logical_resource_id: '+str(cfn_model.resources[r].logical_resource_id)+lineno())
                print('metadata: '+str(cfn_model.resources[r].metadata)+lineno())
                print(str(vars(cfn_model.resources[r]))+lineno())
                print(str(cfn_model.resources[r].raw_model.raw_model)+lineno())
                print("##################################################\n")

            print("\n##################################################")
            print('properties wired into model element objects'+lineno())
            print("##################################################\n")

        if self.debug:

            print("\n##################################################")
            print('Transforming hash into parameters'+lineno())
            print("##################################################\n")

        # Transform cloudformation parameters into parameters object
        cfn_model = self.transform_hash_into_parameters(cloudformation_yml,cfn_model)


        if self.debug:
            print("\n##################################################")
            print('Done transforming hash into parameters' + lineno())
            print('Beginning post process resource model elements' + lineno())
            print("##################################################\n")

        # pass 2: tie together separate resources only where necessary to make life easier for rule logic
        cfn_model = self.post_process_resource_model_elements(cfn_model)

        if self.debug:
            print("\n##################################################")
            print('Done Post processing resource model elements' + lineno())
            print('Beginning to apply parameter values to model' + lineno())
            print("##################################################\n")

        cfn_model = self.apply_parameter_values(cfn_model, parameter_values_json)

        if self.debug:
            print("\n##################################################")
            print('Done applying parameter values to model' + lineno())
            print("##################################################\n")


        return cfn_model


    def apply_parameter_values(self, cfn_model, parameter_values_json):
        """
        ???
        :param cfn_model: 
        :param parameter_values_json: 
        :return: 
        """
        if self.debug:
            print('CfnParser - apply_parameter_values'+lineno())
            print('parameter_values_json: '+str(parameter_values_json)+lineno())

            if parameter_values_json:
                print('parameter values json: '+str(parameter_values_json)+lineno())

        return cfn_model

    def post_process_resource_model_elements(self, cfn_model):
        """
        Post process the resource model elements
        :param cfn_model: 
        :return: 
        """
        if self.debug:
            print("\n\n#######################################################")
            print('CfnParser - post_process_resource_model_elements'+lineno())
            print("##########################################################\n\n")

        resource_parser_class = ParserRegistry(debug=self.debug)

        for r in cfn_model.resources:

            if self.debug:
                print("\n\n####################################")
                print("Processing cfn_model.resource: "+str(r)+lineno())
                print("########################################\n")

                print('resource type: '+str(type(cfn_model.resources[r].resource_type))+lineno())
                print('cfn_model: '+str(cfn_model.resources[r].resource_type)+lineno())
                print('parser registry:'+str(resource_parser_class.registry)+lineno())

            # if there is a resource parser in the registry
            if cfn_model.resources[r].resource_type in resource_parser_class.registry:

                if self.debug:
                    print('found it the resource parser we were looking for '+lineno())
                    print(cfn_model.resources[r].resource_type)
                    print(resource_parser_class.registry[cfn_model.resources[r].resource_type])

                    print("\n\n############################")
                    print('Parsing resource: '+str(r)+lineno())
                    print('type: '+str(resource_parser_class.registry[cfn_model.resources[r].resource_type])+lineno())
                    print("################################\n")

                resource_parser = resource_parser_class.registry[cfn_model.resources[r].resource_type]

                resource_parser.parse(cfn_model, cfn_model.resources[r], debug=self.debug)

        if self.debug:
            print('done parsing the cfn model')

        return cfn_model


    def transform_hash_into_model_elements(self, cfn_hash, cfn_model):
        """
        We are iterating the the resources in the cloudformation template
        and trying to create objects out of each resource, and then putting
        the objects in to the model object
        :param cfn_hash: 
        :param cfn_model: 
        :return: 
        """
        if self.debug:
            print('CfnParser - transform_hash_into_model_elements'+lineno())
            print('hash: '+str(cfn_hash)+lineno())
            print('cfn_model: '+str(cfn_model)+lineno())


        if type(cfn_hash) == type(str()):
            json_acceptable_string = cfn_hash.replace("'", "\"")
            cfn_hash= json.loads(json_acceptable_string)



        # Iterate through each of the resources
        for resource_type in cfn_hash['resource']:

            if self.debug:
                print('resource_type: '+str(resource_type)+lineno())


            for resource_name in cfn_hash['resource'][resource_type]:

                # Create a new resource class based on the name of the resource
                # Does this by getting the resource type, and creating object based on resource type
                resource_class = self.class_from_type_name(resource_type,resource_name)

                resource_class.raw_model= cfn_model

                if self.debug:
                    print('Setting logical resource id to: '+str(resource_name)+lineno())
                resource_class.logical_resource_id = resource_name


                resource_class.resource_type = resource_type
                if 'metadata' in cfn_hash['resource'][resource_type][resource_name]:
                    resource_class.metadata = cfn_hash['resource'][resoure_type][resource_name]['metadata']

                resource_class = self.assign_fields_based_upon_properties(resource_class, cfn_hash['resource'][resource_type][resource_name])

                cfn_model.resources[resource_name]=resource_class

                if self.debug:
                    print("\n\n################################################")
                    print('The new resource object which is being added to cfn_model.resources has the following properties'+lineno())
                    print(type(resource_class))
                    print(vars(resource_class))
                    print(dir(resource_class))
                    print('resource_type: '+str(resource_class.resource_type)+lineno())
                    print('logical_resource_id: '+str(resource_class.logical_resource_id)+lineno())
                    print("##############################################################\n")

        return cfn_model

    def transform_hash_into_parameters(self, cfn_hash, cfn_model):
        """
        Transform hash into parameters
        :param cfn_hash: 
        :param cfn_model: 
        :return: 
        """

        if self.debug:
            print('CfnParser - transform_hash_into_parameters'+lineno())
            print('cfn_hash: '+str(cfn_hash)+lineno())
            print('type hash: '+str(type(cfn_hash))+lineno())
            print('cfn_model: '+str(cfn_model)+lineno())

        if type(cfn_hash) == type(str()):
            json_acceptable_string = cfn_hash.replace("'", "\"")
            cfn_hash= json.loads(json_acceptable_string)

        if 'variable' in cfn_hash:

            for variable in cfn_hash['variable']:

                parameter = Parameter(debug=self.debug)
                parameter.id = variable

                if self.debug:
                    print('parameter id: ' + str(parameter.id) + lineno())

                for param in cfn_hash['variable'][variable]:

                    if self.debug:
                        print("\n###############################")
                        print('param: '+str(param)+lineno())
                        print('value: '+str(cfn_hash['variable'][variable][param])+lineno())
                        print("##################################\n")

                    if param == 'default':
                        parameter.type = str(type(cfn_hash['variable'][variable][param]))
                    else:
                        if self.debug:
                            print('no default parameter'+lineno())

                    if self.debug:
                        print('adding parameter: '+str(param)+'='+str(cfn_hash['variable'][variable][param])+lineno())

                    parameter.instance_variables.append(param+'='+str(cfn_hash['variable'][variable][param]))

                cfn_model.parameters[param] = parameter


        return cfn_model


    def pre_validate_model(self, cloudformation_yml):
        """
        Prevalidate the cloudformation template
        :param cloudformation_yml: 
        :return: 
        """

        if self.debug:
            print("\n\n######################################")
            print('CfnParser - pre_validate_model'+lineno())
            print('########################################\n\n')
            print('cloudformation_yml: '+str(cloudformation_yml)+lineno())

        validator = CloudformationValidator.CloudformationValidator(debug=self.debug)

        errors = validator.validate(cloudformation_yml)

        if errors and len(errors)>0:

            try:

                raise ParserError('Basic CloudFormation syntax error', errors,debug=self.debug)
            except ParserError as e:
                tb = sys.exc_info()[-1]
                if self.debug:
                    print('tb: '+str(tb)+lineno())
                    print('to hash: '+str(e.to_hash())+lineno())
                stk = traceback.extract_tb(tb, 1)
                if self.debug:
                    print('stk: '+str(stk)+lineno())
                fname = stk[0][2]
                if self.debug:
                    print('The failing function was', fname,lineno())
                    print('parser error '+lineno())
                # FIXME
                raise ParserError('Basic CloudFormation syntax error', errors,debug=self.debug)


    def validate_references(self, cfn_hash):
        """
        Validate references in the cloudformation template
        :param cfn_hash: 
        :return: 
        """
        if self.debug:
            print("\n\n###########################################")
            print('CfnParser - validate_references'+lineno())
            print('Looking for unresolved references')
            print('cfn_hash len: '+str(len(cfn_hash))+lineno())
            print("################################################\\n\n")

        ref_validator = ReferenceValidator.ReferenceValidator(debug=self.debug)
        unresolved_refs = ref_validator.unresolved_references(cfn_hash)

        if unresolved_refs and len(unresolved_refs)>0:
            raise ParserError("Unresolved logical resource ids: "+str(unresolved_refs))

    def assign_fields_based_upon_properties(self, resource_object, resource):
        """
        Assign fields in the object based on properties in the resource
        :param resource_object: 
        :param resource: 
        :return: 
        """

        if self.debug:
            print("\n\n#######################################################")
            print('CfnParser - assign_fields_based_upon_properties'+lineno())
            print("#########################################################\n\n")

            print('resource_object: '+str(resource_object)+lineno())
            print('resource: '+str(resource)+lineno())
            print('resource_type:'+str(resource))

        resource_type = str(resource)

        if self.debug:
            print('resource_object dir: '+str(dir(resource_object))+lineno())
            print('resource_object vars: '+str(vars(resource_object))+lineno())

        if 'Properties' in resource:

            if self.debug:
                print("\\n\n\n\n########################################")
                print('resource type: '+str(resource_type)+lineno())
                print("##############################################\n\n\n\n")

            for p in resource['Properties']:

                new_property_name = self.map_property_name_to_attribute(p)

                if self.debug:
                    print("\n\n###########################################")
                    print('Creating object attribute during mapping'+lineno())
                    print('property: '+str(p))
                    print('property details: '+str(resource['Properties'][p]))
                    print('dir:'+str(dir(resource_object))+lineno())
                    print('new property name'+str(new_property_name)+lineno())
                    print("###############################################\n")

                setattr(resource_object, new_property_name, resource['Properties'][p] )

        if self.debug:
            print("\n\n#############################################")
            print('The new resource object now has the following properties'+lineno())
            if hasattr(resource_object, 'policies'):
                print(resource_object.policies)

            if hasattr(resource_object, 'policy_objects'):
                print(resource_object.policy_objects)
            if hasattr(resource_object, 'group_names'):
                print(resource_object.group_names)
            if hasattr(resource_object, 'groups'):
                print(resource_object.groups)
            if hasattr(resource_object, 'resource_type'):
                print(resource_object.resource_type)
            if hasattr(resource_object, 'policy_document'):
                print(resource_object.policy_document)
            print(vars(resource_object))
            print("##################################################\n")

        return resource_object

    def map_property_name_to_attribute(self, string):
        """
        Mapp properties to attributes
        :param string: 
        :return: 
        """

        if self.debug:
            print('property name: '+str(string)+lineno())

        first_character = str(string)[:1]

        if self.debug:
            print('first character: '+str(first_character)+lineno())

        first_character=first_character.lower()
        remaining_characters = string[1:]

        new_property_name = str(first_character)+str(remaining_characters)
        new_property_name.replace('-','_')

        if self.debug:
            print('new_property_name: '+str(new_property_name)+lineno())

        return new_property_name


    def class_from_type_name(self, type_name, cfn_model):
        """
        Create class from type name
        :param type_name: 
        :param cfn_model: 
        :return: 
        """

        if self.debug:
            print('CfnParser - class_from_type_name'+lineno())
            print('type_name: '+str(type_name)+lineno())

        resource_class = self.generate_resource_class_from_type(type_name,cfn_model)

        return resource_class

    def generate_resource_class_from_type(self, type_name, cfn_model):
        """
        Generate resource class from type
        :param type_name: 
        :param cfn_model: 
        :return: 
        """

        if self.debug:
            print('generate_resource_class_from_type'+lineno())
            print('cfn model: '+str(cfn_model)+lineno())
            print('type name: '+str(type_name)+lineno())


        models = [
            'S3BucketPolicy',
            'EC2Instance',
            'EC2NetworkInterface',
            'IAMGroup',
            'IAMManagedPolicy',
            'IAMPolicy',
            'IAMRole',
            'IAMUser',
            'ElasticLoadBalancingLoadBalancer',
            'ElasticLoadBalancingV2LoadBalancer',
            'SQSQueuePolicy',
            'EC2SecurityGroup',
            'EC2SecurityGroupEgress',
            'EC2SecurityGroupIngress',
            'SNSTopicPolicy'
        ]

        models2= [
            'aws_instance',
            'aws_elb',
            'aws_security_group',
            'aws_security_group_rule'
        ]
        module_name = 'AWS'

        if type_name == 'aws_instance':
            short_name ='EC2Instance'
        if type_name == 'aws_elb':
            short_name = 'ElasticLoadBalancingLoadBalancer'
        if type_name == 'aws_security_group':
            short_name = 'EC2SecurityGroup'
        if type_name == 'aws_security_group_rule':
            if type == 'x':
                short_name = 'AWS::EC2::SecurityGroupEgress'
            else:
                short_name = 'AWS::EC2::SecurityGroupIngress'

        #module_names = type_name.split('::')
        if module_name == 'Custom':

            if self.debug:
                print('module is custom: '+lineno())


            custom_resource_class_name = self.initial_upper(short_name)
            resource_class = ModelElement.ModelElement(debug=self.debug)
            setattr(resource_class,'__name__',custom_resource_class_name)
            setattr(resource_class,'debug',self.debug)
        elif module_name == 'AWS':

            if self.debug:
                print('module is AWS: '+lineno())


            if str(type_name) in models2:

                if self.debug:
                    print('short_name: ' + str(short_name) + lineno())
                    print('sys modules __name__: '+str(sys.modules[__name__])+lineno())

                resource_class = getattr(sys.modules[__name__], short_name).__getattribute__(short_name)(cfn_model)
                setattr(resource_class,'debug',self.debug)

            else:
                resource_class = ModelElement.ModelElement(cfn_model)
                setattr(resource_class, '__name__', type_name)
                setattr(resource_class,'debug',self.debug)
        else:
            print('unknown namespace in resource type'+lineno())
            sys.exit(1)

        if self.debug:
            print('vars: '+str(vars(resource_class))+lineno())

        return resource_class


    def initial_upper(self, string):
        """
        First character to upper case
        :param string: 
        :return: 
        """
        if self.debug:
            print('CfnParser - initial_upper'+lineno())

        first_character = str(string)[:1]
        remaining_characters = string[1:]

        new_property_name = str(first_character.upper())+str(remaining_characters)

        return new_property_name