# spring-mysql

## 组件
- [mybatis-plus 3.5.12](https://github.com/baomidou/mybatis-plus)
- [dynamic-datasource 4.3.1](https://github.com/baomidou/dynamic-datasource)
- [mybatis 3.5.19](https://github.com/mybatis/mybatis-3)
- [hikari 4.0.3](https://github.com/brettwooldridge/HikariCP)
- [p6spy 3.9.1](https://github.com/p6spy/p6spy)
- [jdbc mysql-connector-java 8.0.33](https://github.com/mysql/mysql-connector-j)

## 配置说明
数据库连接配置
```yml
spring.datasource.dynamic.datasource.primary = master # 默认库

# 主库
spring.datasource.dynamic.datasource.master.username = root
spring.datasource.dynamic.datasource.master.password = workdock
spring.datasource.dynamic.datasource.master.url = jdbc:mysql://localhost:3306/sprival
spring.datasource.dynamic.datasource.master.driver-class-name = com.mysql.jdbc.Driver
spring.datasource.dynamic.datasource.master.type = com.zaxxer.hikari.HikariDataSource #使用Hikaricp

# 从库
spring.datasource.dynamic.datasource.slave.username = root
spring.datasource.dynamic.datasource.slave.password = workdock
spring.datasource.dynamic.datasource.slave.url = jdbc:mysql://localhost:3306/sprival
spring.datasource.dynamic.datasource.slave.driver-class-name = com.mysql.jdbc.Driver
spring.datasource.dynamic.datasource.slave.type = com.zaxxer.hikari.HikariDataSource #使用Hikaricp
```

hikari线程池配置
```yml
## hikari全局配置
spring.datasource.dynamic.hikari.is-auto-commit =  true
spring.datasource.dynamic.hikari.max_lifetime = 30000
spring.datasource.dynamic.hikari.min_idle = 10
spring.datasource.dynamic.hikari.max_pool_size = 1000
spring.datasource.dynamic.hikari.idle_timeout = 10000
spring.datasource.dynamic.hikari.connection_timeout = 10000
spring.datasource.dynamic.hikari.validation_timeout = 1000
spring.datasource.dynamic.hikari.connection_init_sql = set session wait_timeout=28800,interactive_timeout=28800;

## hikari指定数据库配置
spring.datasource.dynamic.datasource.master.hikari.is-auto-commit =  true
spring.datasource.dynamic.datasource.master.hikari.max_lifetime = 30000
spring.datasource.dynamic.datasource.master.hikari.min_idle = 10
spring.datasource.dynamic.datasource.master.hikari.max_pool_size = 1000
spring.datasource.dynamic.datasource.master.hikari.idle_timeout = 10000
spring.datasource.dynamic.datasource.master.hikari.connection_timeout = 10000
spring.datasource.dynamic.datasource.master.hikari.validation_timeout = 1000
spring.datasource.dynamic.datasource.master.hikari.connection_init_sql = set session wait_timeout=28800,interactive_timeout=28800;
```

hikari线程池配置说明
- autoCommit: 事务自动提交，默认值TRUE
- connectionTimeout: 从连接池拿连接的超时时长, 最小值250毫秒，默认30秒
- idleTimeout：空闲连接超时时间，超过最小空闲连接数的连接空闲保持的存活的时长，单位毫秒，最小值10秒， 默认值10分钟
- maxLifetime：最小空闲连接保持存活的最大时长，这个值应该小于数据库允许客户端连接存活的最大时长，单位毫秒，最小值30秒，默认值30分钟
- connectionTestQuery：用于驱动不支持JDBC4 连接检查Connection.isValid()接口，用于心跳检查
- minimumIdle：最小空闲连接，默认值和maximumPoolSize。建议和maximumPoolSize一样，作为固定连接池使用
- maximumPoolSize：最大连接数，应用请求超过最大连接数的时候，会等待connectionTimeout再抛出异常

> 最小空闲连接：假设minimumIdle=10，maximumPoolSize=15，应用一直占用10个连接，那么hikari会参试创建10个空闲连接，但是受到最大连接数限制，只会创建5个空闲连接
> 假设应用释放了这个10个连接，由于最小空闲连接数是10个，hikari会关掉5个空闲连接

参考文档：[https://github.com/brettwooldridge/HikariCP/tree/HikariCP-3.4.5](https://github.com/brettwooldridge/HikariCP/tree/HikariCP-3.4.5)


## 监控设置
spring boot的actuate的HikariDataSourceMetricsConfiguration自动注入了micrometer的MeterRegistry
访问http://127.0.0.1/api/actuator/metrics就能看到hikaricp的指标

```text
    "hikaricp.connections",
    "hikaricp.connections.acquire",
    "hikaricp.connections.active",
    "hikaricp.connections.creation",
    "hikaricp.connections.idle",
    "hikaricp.connections.max",
    "hikaricp.connections.min",
    "hikaricp.connections.pending",
    "hikaricp.connections.timeout",
    "hikaricp.connections.usage",
```


## 源码分析
[mybatis-plus](./mybatis-plus/README.md)