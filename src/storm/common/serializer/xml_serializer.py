import xml.etree.ElementTree as ET

class XMLSerializer:
    """
    A utility class for serializing and deserializing data to and from XML format.
    """

    @staticmethod
    def serialize(data):
        """
        Serializes a dictionary into XML format.

        :param data: The data to be serialized, typically a dictionary.
        :return: A string representing the serialized XML data.
        """
        root_name = 'root'
        root = ET.Element(root_name)
        XMLSerializer._build_tree(root, data)
        return ET.tostring(root, encoding='unicode')

    @staticmethod
    def deserialize(xml_data):
        """
        Deserializes an XML string into a Python dictionary.

        :param xml_data: The XML string to be deserialized.
        :return: A Python dictionary corresponding to the deserialized XML data.
        """
        root = ET.fromstring(xml_data)
        return XMLSerializer._parse_tree(root)

    @staticmethod
    def _build_tree(element, data):
        """
        Recursively builds an XML tree from a dictionary.

        :param element: The current XML element.
        :param data: The current level of data to serialize.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(element, key)
                XMLSerializer._build_tree(child, value)
        elif isinstance(data, list):
            for item in data:
                child = ET.SubElement(element, 'item')
                XMLSerializer._build_tree(child, item)
        else:
            element.text = str(data)

    @staticmethod
    def _parse_tree(element):
        """
        Recursively parses an XML element into a dictionary.

        :param element: The current XML element to parse.
        :return: A Python object representing the parsed data.
        """
        if len(element):
            result = {}
            for child in element:
                result[child.tag] = XMLSerializer._parse_tree(child)
            return result
        else:
            return element.text
