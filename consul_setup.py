import consul

c = consul.Consul()

c.kv.put('hazelcast/logging/cluster_name', 'logging-cluster')
c.kv.put('hazelcast/logging/members', '127.0.0.1:5701,127.0.0.1:5702,127.0.0.1:5703')
c.kv.put('messaging/queue/cluster_name', 'messaging-cluster')
c.kv.put('messaging/queue/members', '127.0.0.1:5801,127.0.0.1:5802')
c.kv.put('messaging/queue/queue_name', 'messages-queue')