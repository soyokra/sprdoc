# mongo

## 配置说明

mongodb有两种配置方式，一种是host配置，一种是uri配置

host配置只支持单点模式的mongodb服务，并且无法配置额外的一些参数。

```properties
spring.data.mongodb.host = host
spring.data.mongodb.port = port
spring.data.mongodb.username = username
spring.data.mongodb.password = password
spring.data.mongodb.database = database
spring.data.mongodb.authentication-database = authenticationDatabase
spring.data.mongodb.replica-set-name = replicaSetName
```

uri配置可以支持副本集的mongodb服务，并且支持丰富的可选配置项。
```properties
spring.data.mongodb.uri = mongodb://username:password@10.1.100.101:27000,10.1.100.102:27000,10.1.100.103:27000/admin?replicaSet=test&authSource=admin&maxpoolsize=10&minpoolsize=2
```

标准的mongodb uri 格式：

```plaintext
mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
```


### 配置项说明

> 对应的java类是org.springframework.boot.autoconfigure.mongo.MongoProperties


- spring.data.mongodb.host: Mongo server host. Cannot be set with URI.
- spring.data.mongodb.port: Mongo server port. Cannot be set with URI.
- spring.data.mongodb.uri: Mongo database URI. Cannot be set with host, port, credentials and replica set name.
- spring.data.mongodb.database：Database name.
- spring.data.mongodb.authentication-database: Authentication database name.
- spring.data.mongodb.username: Login user of the mongo server. Cannot be set with URI.
- spring.data.mongodb.password: Login password of the mongo server. Cannot be set with URI.
- spring.data.mongodb.replica-set-name: Required replica set name for the cluster. Cannot be set with URI.
- spring.data.mongodb.field-naming-strategy: Fully qualified name of the FieldNamingStrategy to use.
- spring.data.mongodb.grid-fs-database: GridFS database name.
- spring.data.mongodb.uuid-representation: Representation to use when converting a UUID to a BSON binary value.
- spring.data.mongodb.auto-index-creation: Whether to enable auto-index creation.


### uri可选参数说明

> 对应的java类是com.mongodb.ConnectionString

Server Selection Configuration:
- serverSelectionTimeoutMS=ms: How long the driver will wait for server selection to succeed before throwing an exception.
- localThresholdMS=ms: When choosing among multiple MongoDB servers to send a request, the driver will only send that request to a server whose ping time is less than or equal to the server with the fastest ping time plus the local threshold.

Server Monitoring Configuration:
- heartbeatFrequencyMS=ms: The frequency that the driver will attempt to determine the current state of each server in the cluster.

Replica set configuration:
- replicaSet=name: Implies that the hosts given are a seed list, and the driver will attempt to find all members of the set.

Connection Configuration:
- ssl=true|false: Whether to connect using TLS.
- tls=true|false: Whether to connect using TLS. Supersedes the ssl option
- tlsInsecure=true|false: If connecting with TLS, this option enables insecure TLS connections. Currently this has the same effect of setting tlsAllowInvalidHostnames to true. Other mechanism for relaxing TLS security constraints must be handled in the application by customizing the javax. net. ssl. SSLContext
- sslInvalidHostNameAllowed=true|false: Whether to allow invalid host names for TLS connections.
- tlsAllowInvalidHostnames=true|false: Whether to allow invalid host names for TLS connections. Supersedes the sslInvalidHostNameAllowed option
- connectTimeoutMS=ms: How long a connection can take to be opened before timing out.
- socketTimeoutMS=ms: How long a send or receive on a socket can take before timing out.
- maxIdleTimeMS=ms: Maximum idle time of a pooled connection. A connection that exceeds this limit will be closed
- maxLifeTimeMS=ms: Maximum life time of a pooled connection. A connection that exceeds this limit will be closed

Connection pool configuration:
- maxPoolSize=n: The maximum number of connections in the connection pool.
- waitQueueTimeoutMS=ms: The maximum wait time in milliseconds that a thread may wait for a connection to become available.

Write concern configuration:
- safe=true|false
  - true: the driver ensures that all writes are acknowledged by the MongoDB server, or else throws an exception. (see also w and wtimeoutMS).
  - false: the driver does not ensure that all writes are acknowledged by the MongoDB server.
- journal=true|false
  - true: the driver waits for the server to group commit to the journal file on disk.
  - false: the driver does not wait for the server to group commit to the journal file on disk.
- w=wValue
  - The driver adds { w : wValue } to all write commands. Implies safe=true.
  - wValue is typically a number, but can be any string in order to allow for specifications like "majority"
- wtimeoutMS=ms
  - The driver adds { wtimeout : ms } to all write commands. Implies safe=true.
  - Used in combination with w

Read preference configuration:
- readPreference=enum: The read preference for this connection.
  - Enumerated values:
    - primary
    - primaryPreferred
    - secondary
    - secondaryPreferred
    - nearest
- readPreferenceTags=string. A representation of a tag set as a comma-separated list of colon-separated key-value pairs, e. g. "dc:ny,rack:1". Spaces are stripped from beginning and end of all keys and values. To specify a list of tag sets, using multiple readPreferenceTags, e. g. readPreferenceTags=dc:ny,rack:1;readPreferenceTags=dc:ny;readPreferenceTags=
Note the empty value for the last one, which means match any secondary as a last resort.
Order matters when using multiple readPreferenceTags.
- maxStalenessSeconds=seconds. The maximum staleness in seconds. For use with any non-primary read preference, the driver estimates the staleness of each secondary, based on lastWriteDate values provided in server isMaster responses, and selects only those secondaries whose staleness is less than or equal to maxStalenessSeconds. Not providing the parameter or explicitly setting it to -1 indicates that there should be no max staleness check. The maximum staleness feature is designed to prevent badly-lagging servers from being selected. The staleness estimate is imprecise and shouldn't be used to try to select "up-to-date" secondaries. The minimum value is either 90 seconds, or the heartbeat frequency plus 10 seconds, whichever is greatest.

Authentication configuration:
- authMechanism=MONGO-CR|GSSAPI|PLAIN|MONGODB-X509: The authentication mechanism to use if a credential was supplied. The default is unspecified, in which case the client will pick the most secure mechanism available based on the sever version. For the GSSAPI and MONGODB-X509 mechanisms, no password is accepted, only the username.
- authSource=string: The source of the authentication credentials. This is typically the database that the credentials have been created. The value defaults to the database specified in the path portion of the connection string. If the database is specified in neither place, the default value is "admin". This option is only respected when using the MONGO-CR mechanism (the default).
- authMechanismProperties=PROPERTY_NAME:PROPERTY_VALUE,PROPERTY_NAME2:PROPERTY_VALUE2: This option allows authentication mechanism properties to be set on the connection string.
- gssapiServiceName=string: This option only applies to the GSSAPI mechanism and is used to alter the service name. Deprecated, please use authMechanismProperties=SERVICE_NAME:string instead.

Server Handshake configuration:
- appName=string: Sets the logical name of the application. The application name may be used by the client to identify the application to the server, for use in server logs, slow query logs, and profile collection.

Compressor configuration:
- compressors=string: A comma-separated list of compressors to request from the server. The supported compressors currently are 'zlib', 'snappy' and 'zstd'.
- zlibCompressionLevel=integer: Integer value from -1 to 9 representing the zlib compression level. Lower values will make compression faster, while higher values will make compression better.

General configuration:
- retryWrites=true|false. If true the driver will retry supported write operations if they fail due to a network error. Defaults to true.
- retryReads=true|false. If true the driver will retry supported read operations if they fail due to a network error. Defaults to true.
- uuidRepresentation=unspecified|standard|javaLegacy|csharpLegacy|pythonLegacy. See MongoClientSettings. getUuidRepresentation() for documentation of semantics of this parameter. Defaults to "javaLegacy", but will change to "unspecified" in the next major release.

## 监控预警

### 监控指标
- mongodb_driver_commands_seconds_count: counter
- mongodb_driver_commands_seconds_max: gauge
- mongodb_driver_commands_seconds_sum: gauge
- mongodb_driver_pool_checkedout: gauge; the count of connections that are currently in use
- mongodb_driver_pool_size: gauge; the current size of the connection pool, including idle and  in-use members
- mongodb_driver_pool_waitqueuesize: gauge; the current size of the wait queue for a connection from the pool

### PromSQL配置
```promSQL
# 平均耗时
avg(rate(mongodb_driver_commands_seconds_sum[5m]) / rate(mongodb_driver_commands_seconds_count[5m])) by (job)

# 命令执行时间 TOP 20
topk(20, mongodb_driver_commands_seconds_max)

# 使用中的连接数
sum(mongodb_driver_pool_checkedout) by (job)

# 连接池的总大小
sum(mongodb_driver_pool_size) by (job)

# 当前等待从连接池获取连接的请求数量
sum(mongodb_driver_pool_waitqueuesize) by (job)
```