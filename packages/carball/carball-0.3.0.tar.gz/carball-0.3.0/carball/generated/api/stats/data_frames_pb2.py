# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/stats/data_frames.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ...api import game_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='api/stats/data_frames.proto',
  package='api.stats',
  serialized_pb=_b('\n\x1b\x61pi/stats/data_frames.proto\x12\tapi.stats\x1a\x0e\x61pi/game.proto:\x1e\n\x0b\x64\x61ta_frames\x12\t.api.Game\x18\x64 \x01(\x0c')
  ,
  dependencies=[game_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DATA_FRAMES_FIELD_NUMBER = 100
data_frames = _descriptor.FieldDescriptor(
  name='data_frames', full_name='api.stats.data_frames', index=0,
  number=100, type=12, cpp_type=9, label=1,
  has_default_value=False, default_value=_b(""),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)

DESCRIPTOR.extensions_by_name['data_frames'] = data_frames

game_pb2.Game.RegisterExtension(data_frames)

# @@protoc_insertion_point(module_scope)
