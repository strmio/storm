import io
import fastavro
from fastavro.schema import load_schema

class AvroSerializer:
    """
    A utility class for serializing and deserializing data to and from Avro format using a predefined schema.
    """

    def __init__(self, schema_path):
        """
        Initializes the AvroSerializer with the given Avro schema.

        :param schema_path: The file path to the Avro schema (.avsc file).
        """
        self.schema = load_schema(schema_path)

    def serialize(self, data):
        """
        Serializes the given data into Avro format using the schema.

        :param data: The data to be serialized, typically a dictionary.
        :return: A byte array representing the serialized Avro data.
        """
        bytes_writer = io.BytesIO()
        fastavro.writer(bytes_writer, self.schema, [data])
        return bytes_writer.getvalue()

    def deserialize(self, data):
        """
        Deserializes the given Avro byte array into a Python object using the schema.

        :param data: The Avro byte array to be deserialized.
        :return: A Python object corresponding to the deserialized Avro data.
        """
        bytes_reader = io.BytesIO(data)
        reader = fastavro.reader(bytes_reader, self.schema)
        return next(reader)
