import sys
sys.path.insert(0,'gen')
import common_pb2,gateway_pb2
t=common_pb2.Timestamp(seconds=1700000000,nanos=321)
r=gateway_pb2.RouteRequest(route_id='sample',payload=b'hello',sent_at=t)
assert gateway_pb2.RouteRequest.FromString(r.SerializeToString())==r
reply=gateway_pb2.RouteReply(accepted=True,error=common_pb2.Error(code=0,message='ok'))
assert gateway_pb2.RouteReply.FromString(reply.SerializeToString()).accepted
assert gateway_pb2.DESCRIPTOR.services_by_name['Gateway'].methods_by_name['Route'].input_type.full_name=='acme.gateway.v1.RouteRequest'
print('protobuf verification passed')
