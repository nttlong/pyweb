from xml.dom import minidom
def parse_to_dict(xml):
    ret = {}
    if not hasattr(xml,"attributes"):
        return xml.data
    if xml == None:
        return xml
    if xml.childNodes.length >0:
        nodes = [n for n in xml.childNodes if hasattr(n,"tagName")]
        for node in nodes:

            if not hasattr(node,"attributes") and node.childNodes.length == 1:
                ret.update({
                    node.tagName:node.childNodes[0].data
                })
            elif node.attributes.has_key("type") and\
                    node.attributes.get("type").value == "list":
                ret_list =[]
                for cNode in node.childNodes:
                    p_node =parse_to_dict(cNode)
                    if p_node!=None:
                        ret_list.append(p_node)
                ret.update ({
                    node.tagName: ret_list
                })
            else:
                ret_data = parse_to_dict (node)
                ret.update ({
                    node.tagName: ret_data
                })
        return ret
    elif hasattr(xml,"attributes") and \
            xml.attributes != None and  \
            xml.attributes.has_key("value"):
        if xml.attributes.get("type",None)!= None and\
                xml.attributes.get("type").value == "list":
            ret ={}
            ret_list = []
            for cNode in xml.childNodes:
                ret_list.append (parse_to_dict (cNode))
            ret.update ({
                xml.tagName: ret_list
            })
            return ret
        elif not xml.attributes.has_key("type"):
            return xml.attributes.get("value").value
        else:
            type =__builtins__.get(xml.attributes.get("type").value)
            return type(xml.attributes.get ("value").value)
    elif xml.childNodes.length==1:
        return xml.childNodes[0].data
def load(file_path):
    xml = minidom.parse(file_path)
    return parse_to_dict(xml.childNodes[0])

