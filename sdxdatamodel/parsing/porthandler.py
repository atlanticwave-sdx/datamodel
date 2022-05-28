import json
from sdxdatamodel.models.port import Port
from .exceptions import MissingAttributeException

class PortHandler():

    """"
    Handler for parsing the connection request descritpion in json 
    """

    def __init__(self):
        super().__init__()
        self.port = None

    def import_port_data(self, data):
        l = None
        l_r=None
        p_a=None
        s_n=None
        try:
            id = data['id']
            name=data['name']
            node=data['node']

            if 'short_name' in data.keys():
                s_n=data['short_name']
            if 'label' in data.keys():  
                l=data['label']
            if 'label_range' in data.keys():  
                l_r=data['label_range']
            if 'private_attributes' in data.keys():     
                p_a=data['private_attributes']
        except KeyError as e:
            raise MissingAttributeException(e.args[0],e.args[0])

        port=Port(id=id, name=name,short_name=s_n, node=node, label=l, label_range=l_r, status=None, private_attributes=p_a)

        return port
    
    def import_port(self,file):
        with open(file, 'r', encoding='utf-8') as data_file:
            data = json.load(data_file)
            self.port = self.import_port_data(data)

    def get_port(self):
        return self.port
