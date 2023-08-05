# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rockset/value.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rockset import document_locator_pb2 as rockset_dot_document__locator__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='rockset/value.proto',
  package='rockset',
  syntax='proto3',
  serialized_pb=_b('\n\x13rockset/value.proto\x12\x07rockset\x1a\x1erockset/document_locator.proto\"\x07\n\x05\x45mpty\"5\n\tDateProto\x12\x0c\n\x04year\x18\x01 \x01(\x03\x12\r\n\x05month\x18\x02 \x01(\x05\x12\x0b\n\x03\x64\x61y\x18\x03 \x01(\x05\"N\n\tTimeProto\x12\x0c\n\x04hour\x18\x01 \x01(\x05\x12\x0e\n\x06minute\x18\x02 \x01(\x05\x12\x0e\n\x06second\x18\x03 \x01(\x05\x12\x13\n\x0bmicrosecond\x18\x04 \x01(\x05\"S\n\rDateTimeProto\x12 \n\x04\x64\x61te\x18\x01 \x01(\x0b\x32\x12.rockset.DateProto\x12 \n\x04time\x18\x02 \x01(\x0b\x32\x12.rockset.TimeProto\"\xf6\x03\n\x05Value\x12\x13\n\tint_value\x18\x01 \x01(\x03H\x00\x12\x15\n\x0b\x66loat_value\x18\x02 \x01(\x01H\x00\x12\x14\n\nbool_value\x18\x03 \x01(\x08H\x00\x12\x16\n\x0cstring_value\x18\x04 \x01(\tH\x00\x12\x15\n\x0b\x62ytes_value\x18\x05 \x01(\x0cH\x00\x12,\n\x0cobject_value\x18\x06 \x01(\x0b\x32\x14.rockset.ObjectValueH\x00\x12*\n\x0b\x61rray_value\x18\x07 \x01(\x0b\x32\x13.rockset.ArrayValueH\x00\x12,\n\x0c\x63ustom_value\x18\x08 \x01(\x0b\x32\x14.rockset.CustomValueH\x00\x12\x14\n\nnull_value\x18\t \x01(\x08H\x00\x12.\n\rlocator_value\x18\n \x01(\x0b\x32\x15.DocumentLocatorProtoH\x00\x12\x19\n\x0ftimestamp_value\x18\x0b \x01(\x03H\x00\x12\x30\n\x0e\x64\x61tetime_value\x18\x0c \x01(\x0b\x32\x16.rockset.DateTimeProtoH\x00\x12(\n\ndate_value\x18\r \x01(\x0b\x32\x12.rockset.DateProtoH\x00\x12(\n\ntime_value\x18\x0e \x01(\x0b\x32\x12.rockset.TimeProtoH\x00\x42\r\n\x0bvalue_union\",\n\x0b\x43ustomValue\x12\x0c\n\x04type\x18\x01 \x01(\r\x12\x0f\n\x07\x65ncoded\x18\x02 \x01(\x0c\"3\n\x05\x46ield\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1d\n\x05value\x18\x02 \x01(\x0b\x32\x0e.rockset.Value\"-\n\x0bObjectValue\x12\x1e\n\x06\x66ields\x18\x01 \x03(\x0b\x32\x0e.rockset.Field\"+\n\nArrayValue\x12\x1d\n\x05value\x18\x02 \x03(\x0b\x32\x0e.rockset.Value\"\x8c\x03\n\x04Type\x12(\n\x04type\x18\x01 \x01(\x0e\x32\x18.rockset.Type.ScalarTypeH\x00\x12*\n\x0bobject_type\x18\x02 \x01(\x0b\x32\x13.rockset.ObjectTypeH\x00\x12(\n\narray_type\x18\x03 \x01(\x0b\x32\x12.rockset.ArrayTypeH\x00\x12*\n\x0b\x63ustom_type\x18\x04 \x01(\x0b\x32\x13.rockset.CustomTypeH\x00\x12\x10\n\x08inferred\x18\x05 \x01(\x08\x12%\n\rdefault_value\x18\x06 \x01(\x0b\x32\x0e.rockset.Value\x12#\n\x0csource_field\x18\x07 \x01(\x0b\x32\r.rockset.Type\x12\x0e\n\x06stored\x18\x08 \x01(\x08\x12\x0f\n\x07indexed\x18\t \x01(\x08\"K\n\nScalarType\x12\x08\n\x04NONE\x10\x00\x12\x07\n\x03INT\x10\x01\x12\t\n\x05\x46LOAT\x10\x02\x12\x08\n\x04\x42OOL\x10\x03\x12\n\n\x06STRING\x10\x04\x12\t\n\x05\x42YTES\x10\x05\x42\x0c\n\ntype_union\"3\n\x07KeyType\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1b\n\x04type\x18\x02 \x01(\x0b\x32\r.rockset.Type\"*\n\nObjectType\x12\x1c\n\x02kt\x18\x01 \x03(\x0b\x32\x10.rockset.KeyType\"(\n\tArrayType\x12\x1b\n\x04type\x18\x01 \x01(\x0b\x32\r.rockset.Type\"\x1a\n\nCustomType\x12\x0c\n\x04type\x18\x01 \x01(\r\"\x1d\n\x0b\x42itSetProto\x12\x0e\n\x06\x62locks\x18\x01 \x03(\x07\x42\x14\n\x10io.rockset.protoP\x00\x62\x06proto3')
  ,
  dependencies=[rockset_dot_document__locator__pb2.DESCRIPTOR,])



_TYPE_SCALARTYPE = _descriptor.EnumDescriptor(
  name='ScalarType',
  full_name='rockset.Type.ScalarType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INT', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FLOAT', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BOOL', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STRING', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BYTES', index=5, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1297,
  serialized_end=1372,
)
_sym_db.RegisterEnumDescriptor(_TYPE_SCALARTYPE)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='rockset.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=64,
  serialized_end=71,
)


_DATEPROTO = _descriptor.Descriptor(
  name='DateProto',
  full_name='rockset.DateProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='year', full_name='rockset.DateProto.year', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='month', full_name='rockset.DateProto.month', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='day', full_name='rockset.DateProto.day', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=73,
  serialized_end=126,
)


_TIMEPROTO = _descriptor.Descriptor(
  name='TimeProto',
  full_name='rockset.TimeProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='hour', full_name='rockset.TimeProto.hour', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='minute', full_name='rockset.TimeProto.minute', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='second', full_name='rockset.TimeProto.second', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='microsecond', full_name='rockset.TimeProto.microsecond', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=128,
  serialized_end=206,
)


_DATETIMEPROTO = _descriptor.Descriptor(
  name='DateTimeProto',
  full_name='rockset.DateTimeProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='date', full_name='rockset.DateTimeProto.date', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='time', full_name='rockset.DateTimeProto.time', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=208,
  serialized_end=291,
)


_VALUE = _descriptor.Descriptor(
  name='Value',
  full_name='rockset.Value',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='int_value', full_name='rockset.Value.int_value', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='float_value', full_name='rockset.Value.float_value', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bool_value', full_name='rockset.Value.bool_value', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_value', full_name='rockset.Value.string_value', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bytes_value', full_name='rockset.Value.bytes_value', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='object_value', full_name='rockset.Value.object_value', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='array_value', full_name='rockset.Value.array_value', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='custom_value', full_name='rockset.Value.custom_value', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='null_value', full_name='rockset.Value.null_value', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='locator_value', full_name='rockset.Value.locator_value', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_value', full_name='rockset.Value.timestamp_value', index=10,
      number=11, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='datetime_value', full_name='rockset.Value.datetime_value', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='date_value', full_name='rockset.Value.date_value', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='time_value', full_name='rockset.Value.time_value', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='value_union', full_name='rockset.Value.value_union',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=294,
  serialized_end=796,
)


_CUSTOMVALUE = _descriptor.Descriptor(
  name='CustomValue',
  full_name='rockset.CustomValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='rockset.CustomValue.type', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='encoded', full_name='rockset.CustomValue.encoded', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=798,
  serialized_end=842,
)


_FIELD = _descriptor.Descriptor(
  name='Field',
  full_name='rockset.Field',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='rockset.Field.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='rockset.Field.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=844,
  serialized_end=895,
)


_OBJECTVALUE = _descriptor.Descriptor(
  name='ObjectValue',
  full_name='rockset.ObjectValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fields', full_name='rockset.ObjectValue.fields', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=897,
  serialized_end=942,
)


_ARRAYVALUE = _descriptor.Descriptor(
  name='ArrayValue',
  full_name='rockset.ArrayValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='rockset.ArrayValue.value', index=0,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=944,
  serialized_end=987,
)


_TYPE = _descriptor.Descriptor(
  name='Type',
  full_name='rockset.Type',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='rockset.Type.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='object_type', full_name='rockset.Type.object_type', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='array_type', full_name='rockset.Type.array_type', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='custom_type', full_name='rockset.Type.custom_type', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='inferred', full_name='rockset.Type.inferred', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='default_value', full_name='rockset.Type.default_value', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source_field', full_name='rockset.Type.source_field', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stored', full_name='rockset.Type.stored', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='indexed', full_name='rockset.Type.indexed', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TYPE_SCALARTYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='type_union', full_name='rockset.Type.type_union',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=990,
  serialized_end=1386,
)


_KEYTYPE = _descriptor.Descriptor(
  name='KeyType',
  full_name='rockset.KeyType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='rockset.KeyType.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='rockset.KeyType.type', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1388,
  serialized_end=1439,
)


_OBJECTTYPE = _descriptor.Descriptor(
  name='ObjectType',
  full_name='rockset.ObjectType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='kt', full_name='rockset.ObjectType.kt', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1441,
  serialized_end=1483,
)


_ARRAYTYPE = _descriptor.Descriptor(
  name='ArrayType',
  full_name='rockset.ArrayType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='rockset.ArrayType.type', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1485,
  serialized_end=1525,
)


_CUSTOMTYPE = _descriptor.Descriptor(
  name='CustomType',
  full_name='rockset.CustomType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='rockset.CustomType.type', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1527,
  serialized_end=1553,
)


_BITSETPROTO = _descriptor.Descriptor(
  name='BitSetProto',
  full_name='rockset.BitSetProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blocks', full_name='rockset.BitSetProto.blocks', index=0,
      number=1, type=7, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1555,
  serialized_end=1584,
)

_DATETIMEPROTO.fields_by_name['date'].message_type = _DATEPROTO
_DATETIMEPROTO.fields_by_name['time'].message_type = _TIMEPROTO
_VALUE.fields_by_name['object_value'].message_type = _OBJECTVALUE
_VALUE.fields_by_name['array_value'].message_type = _ARRAYVALUE
_VALUE.fields_by_name['custom_value'].message_type = _CUSTOMVALUE
_VALUE.fields_by_name['locator_value'].message_type = rockset_dot_document__locator__pb2._DOCUMENTLOCATORPROTO
_VALUE.fields_by_name['datetime_value'].message_type = _DATETIMEPROTO
_VALUE.fields_by_name['date_value'].message_type = _DATEPROTO
_VALUE.fields_by_name['time_value'].message_type = _TIMEPROTO
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['int_value'])
_VALUE.fields_by_name['int_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['float_value'])
_VALUE.fields_by_name['float_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['bool_value'])
_VALUE.fields_by_name['bool_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['string_value'])
_VALUE.fields_by_name['string_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['bytes_value'])
_VALUE.fields_by_name['bytes_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['object_value'])
_VALUE.fields_by_name['object_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['array_value'])
_VALUE.fields_by_name['array_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['custom_value'])
_VALUE.fields_by_name['custom_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['null_value'])
_VALUE.fields_by_name['null_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['locator_value'])
_VALUE.fields_by_name['locator_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['timestamp_value'])
_VALUE.fields_by_name['timestamp_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['datetime_value'])
_VALUE.fields_by_name['datetime_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['date_value'])
_VALUE.fields_by_name['date_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_VALUE.oneofs_by_name['value_union'].fields.append(
  _VALUE.fields_by_name['time_value'])
_VALUE.fields_by_name['time_value'].containing_oneof = _VALUE.oneofs_by_name['value_union']
_FIELD.fields_by_name['value'].message_type = _VALUE
_OBJECTVALUE.fields_by_name['fields'].message_type = _FIELD
_ARRAYVALUE.fields_by_name['value'].message_type = _VALUE
_TYPE.fields_by_name['type'].enum_type = _TYPE_SCALARTYPE
_TYPE.fields_by_name['object_type'].message_type = _OBJECTTYPE
_TYPE.fields_by_name['array_type'].message_type = _ARRAYTYPE
_TYPE.fields_by_name['custom_type'].message_type = _CUSTOMTYPE
_TYPE.fields_by_name['default_value'].message_type = _VALUE
_TYPE.fields_by_name['source_field'].message_type = _TYPE
_TYPE_SCALARTYPE.containing_type = _TYPE
_TYPE.oneofs_by_name['type_union'].fields.append(
  _TYPE.fields_by_name['type'])
_TYPE.fields_by_name['type'].containing_oneof = _TYPE.oneofs_by_name['type_union']
_TYPE.oneofs_by_name['type_union'].fields.append(
  _TYPE.fields_by_name['object_type'])
_TYPE.fields_by_name['object_type'].containing_oneof = _TYPE.oneofs_by_name['type_union']
_TYPE.oneofs_by_name['type_union'].fields.append(
  _TYPE.fields_by_name['array_type'])
_TYPE.fields_by_name['array_type'].containing_oneof = _TYPE.oneofs_by_name['type_union']
_TYPE.oneofs_by_name['type_union'].fields.append(
  _TYPE.fields_by_name['custom_type'])
_TYPE.fields_by_name['custom_type'].containing_oneof = _TYPE.oneofs_by_name['type_union']
_KEYTYPE.fields_by_name['type'].message_type = _TYPE
_OBJECTTYPE.fields_by_name['kt'].message_type = _KEYTYPE
_ARRAYTYPE.fields_by_name['type'].message_type = _TYPE
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['DateProto'] = _DATEPROTO
DESCRIPTOR.message_types_by_name['TimeProto'] = _TIMEPROTO
DESCRIPTOR.message_types_by_name['DateTimeProto'] = _DATETIMEPROTO
DESCRIPTOR.message_types_by_name['Value'] = _VALUE
DESCRIPTOR.message_types_by_name['CustomValue'] = _CUSTOMVALUE
DESCRIPTOR.message_types_by_name['Field'] = _FIELD
DESCRIPTOR.message_types_by_name['ObjectValue'] = _OBJECTVALUE
DESCRIPTOR.message_types_by_name['ArrayValue'] = _ARRAYVALUE
DESCRIPTOR.message_types_by_name['Type'] = _TYPE
DESCRIPTOR.message_types_by_name['KeyType'] = _KEYTYPE
DESCRIPTOR.message_types_by_name['ObjectType'] = _OBJECTTYPE
DESCRIPTOR.message_types_by_name['ArrayType'] = _ARRAYTYPE
DESCRIPTOR.message_types_by_name['CustomType'] = _CUSTOMTYPE
DESCRIPTOR.message_types_by_name['BitSetProto'] = _BITSETPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.Empty)
  ))
_sym_db.RegisterMessage(Empty)

DateProto = _reflection.GeneratedProtocolMessageType('DateProto', (_message.Message,), dict(
  DESCRIPTOR = _DATEPROTO,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.DateProto)
  ))
_sym_db.RegisterMessage(DateProto)

TimeProto = _reflection.GeneratedProtocolMessageType('TimeProto', (_message.Message,), dict(
  DESCRIPTOR = _TIMEPROTO,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.TimeProto)
  ))
_sym_db.RegisterMessage(TimeProto)

DateTimeProto = _reflection.GeneratedProtocolMessageType('DateTimeProto', (_message.Message,), dict(
  DESCRIPTOR = _DATETIMEPROTO,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.DateTimeProto)
  ))
_sym_db.RegisterMessage(DateTimeProto)

Value = _reflection.GeneratedProtocolMessageType('Value', (_message.Message,), dict(
  DESCRIPTOR = _VALUE,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.Value)
  ))
_sym_db.RegisterMessage(Value)

CustomValue = _reflection.GeneratedProtocolMessageType('CustomValue', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMVALUE,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.CustomValue)
  ))
_sym_db.RegisterMessage(CustomValue)

Field = _reflection.GeneratedProtocolMessageType('Field', (_message.Message,), dict(
  DESCRIPTOR = _FIELD,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.Field)
  ))
_sym_db.RegisterMessage(Field)

ObjectValue = _reflection.GeneratedProtocolMessageType('ObjectValue', (_message.Message,), dict(
  DESCRIPTOR = _OBJECTVALUE,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.ObjectValue)
  ))
_sym_db.RegisterMessage(ObjectValue)

ArrayValue = _reflection.GeneratedProtocolMessageType('ArrayValue', (_message.Message,), dict(
  DESCRIPTOR = _ARRAYVALUE,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.ArrayValue)
  ))
_sym_db.RegisterMessage(ArrayValue)

Type = _reflection.GeneratedProtocolMessageType('Type', (_message.Message,), dict(
  DESCRIPTOR = _TYPE,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.Type)
  ))
_sym_db.RegisterMessage(Type)

KeyType = _reflection.GeneratedProtocolMessageType('KeyType', (_message.Message,), dict(
  DESCRIPTOR = _KEYTYPE,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.KeyType)
  ))
_sym_db.RegisterMessage(KeyType)

ObjectType = _reflection.GeneratedProtocolMessageType('ObjectType', (_message.Message,), dict(
  DESCRIPTOR = _OBJECTTYPE,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.ObjectType)
  ))
_sym_db.RegisterMessage(ObjectType)

ArrayType = _reflection.GeneratedProtocolMessageType('ArrayType', (_message.Message,), dict(
  DESCRIPTOR = _ARRAYTYPE,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.ArrayType)
  ))
_sym_db.RegisterMessage(ArrayType)

CustomType = _reflection.GeneratedProtocolMessageType('CustomType', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMTYPE,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.CustomType)
  ))
_sym_db.RegisterMessage(CustomType)

BitSetProto = _reflection.GeneratedProtocolMessageType('BitSetProto', (_message.Message,), dict(
  DESCRIPTOR = _BITSETPROTO,
  __module__ = 'rockset.value_pb2'
  # @@protoc_insertion_point(class_scope:rockset.BitSetProto)
  ))
_sym_db.RegisterMessage(BitSetProto)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\020io.rockset.protoP\000'))
# @@protoc_insertion_point(module_scope)
