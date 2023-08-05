# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rockset/regex.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='rockset/regex.proto',
  package='rockset',
  syntax='proto3',
  serialized_pb=_b('\n\x13rockset/regex.proto\x12\x07rockset\"e\n\x05Regex\x12\x0f\n\x07pattern\x18\x01 \x01(\t\x12)\n\x08\x65ncoding\x18\x02 \x01(\x0e\x32\x17.rockset.Regex.Encoding\" \n\x08\x45ncoding\x12\x08\n\x04UTF8\x10\x00\x12\n\n\x06LATIN1\x10\x01\x42\x14\n\x10io.rockset.protoP\x00\x62\x06proto3')
)



_REGEX_ENCODING = _descriptor.EnumDescriptor(
  name='Encoding',
  full_name='rockset.Regex.Encoding',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UTF8', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LATIN1', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=101,
  serialized_end=133,
)
_sym_db.RegisterEnumDescriptor(_REGEX_ENCODING)


_REGEX = _descriptor.Descriptor(
  name='Regex',
  full_name='rockset.Regex',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pattern', full_name='rockset.Regex.pattern', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='encoding', full_name='rockset.Regex.encoding', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _REGEX_ENCODING,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=133,
)

_REGEX.fields_by_name['encoding'].enum_type = _REGEX_ENCODING
_REGEX_ENCODING.containing_type = _REGEX
DESCRIPTOR.message_types_by_name['Regex'] = _REGEX
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Regex = _reflection.GeneratedProtocolMessageType('Regex', (_message.Message,), dict(
  DESCRIPTOR = _REGEX,
  __module__ = 'rockset.regex_pb2'
  # @@protoc_insertion_point(class_scope:rockset.Regex)
  ))
_sym_db.RegisterMessage(Regex)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\020io.rockset.protoP\000'))
# @@protoc_insertion_point(module_scope)
