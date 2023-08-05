import base64


def replace_b64_in_dict(item):
  """
  Replace base64 string in python dictionary of inference data. Refer to https://github.com/tensorflow/serving/blob/master/tensorflow_serving/g3doc/api_rest.md#encoding-binary-values .
  
  For example: {'inputs': {'images': {'b64': 'YWJjZGVmZ2hpMTIz'}, 'foo': 'bar'}} to {'inputs': {'images': 'abcdefghi123', 'foo': 'bar'}}.
  """

  if isinstance(item, dict):
    for key, value in item.iteritems():
      if isinstance(value, dict) and value.keys()[0] == "b64":
        b64_string = value.values()[0]
        # TODO: unicode string to string
        b64_string = str(b64_string)
        bytearray_string = base64.urlsafe_b64decode(b64_string)
        item[key] = bytearray_string
      else:
        replace_b64_in_dict(value)

  elif isinstance(item, list):
    for index, value in enumerate(item):
      if isinstance(value, dict) and value.keys()[0] == "b64":
        b64_string = value.values()[0]
        b64_string = str(b64_string)
        bytearray_string = base64.urlsafe_b64decode(b64_string)
        item[index] = bytearray_string
      else:
        replace_b64_in_dict(value)
