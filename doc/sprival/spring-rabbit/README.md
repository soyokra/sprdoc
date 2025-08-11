## 监控指标

```text
rabbitmq_acknowledged_published_total
rabbitmq_acknowledged_total
rabbitmq_channels
rabbitmq_connections
rabbitmq_consumed_total
rabbitmq_failed_to_publish_total
rabbitmq_not_acknowledged_published_total
rabbitmq_published_total
rabbitmq_unrouted_published_total
rabbitmq_rejected_total
```

| 指标名称                                      | 类型    | 含义                        |
| ----------------------------------------- | ----- | ------------------------- |
| rabbitmq_published_total                  | count | 发布到 RabbitMQ 的消息总数        |
| rabbitmq_acknowledged_published_total     | count | 已成功被 Broker 接收并确认的消息总数    |
| rabbitmq_not_acknowledged_published_total | count | 未收到 Broker 确认的消息总数        |
| rabbitmq_failed_to_publish_total          | count | 发布失败的消息总数                 |
| rabbitmq_unrouted_published_total         | count | 已发布但因没有匹配队列而被丢弃的消息总数      |
| rabbitmq_consumed_total                   | count | 消费者从队列中获取的消息总数            |
| rabbitmq_acknowledged_total               | count | 消费者已确认（ACK）的消息总数          |
| rabbitmq_rejected_total                   | count | 消费者拒绝（NACK）的消息总数          |
| rabbitmq_connections                      | gauge | 当前与 RabbitMQ 建立的 TCP 连接总数 |
| rabbitmq_channels                         | gauge | 过高的连接数可能导致 Broker 资源耗尽    |

消息流： published_total → acknowledged_published_total → consumed_total → acknowledged_total

#### PromQL

连接池配置指标

```PromQL
# 连接总数
sum(rabbitmq_connections) by (job)

# 信道总数
sum(rabbitmq_connections) by (job)
```

消息发布指标

```PromQL
# 发布成功率
avg((rabbitmq_acknowledged_published_total / rabbitmq_published_total) * 100) by (job)
```

消息消费指标

```PromQL
avg((rabbitmq_rejected_total  / rabbitmq_consumed_total) * 100) by (job)
```

## 源码分析

- org.springframework.amqp：amqp接口定义和公共支持类
- org.springframework.amqp.rabbit: rabbit实现包
- org.springframework.boot.actuate.amqp：rabbit健康检查
- org.springframework.boot.actuate.metrics.amqp：rabbit指标监控
- org.springframework.boot.actuate.autoconfigure.amqp：rabbitmq健康检查自动装配
- org.springframework.boot.autoconfigure.amqp：rabbit自动装配

rabbit自动装配通过spring.factories加载

```text
org.springframework.boot.autoconfigure.amqp.RabbitAutoConfiguration
```

## 监控指标

#### 健康检查

健康检查是通过使用rabbitTemplate尝试获取版本实现的

```java
public class RabbitHealthIndicator extends AbstractHealthIndicator {

    private final RabbitTemplate rabbitTemplate;

    public RabbitHealthIndicator(RabbitTemplate rabbitTemplate) {
        super("Rabbit health check failed");
        Assert.notNull(rabbitTemplate, "RabbitTemplate must not be null");
        this.rabbitTemplate = rabbitTemplate;
    }

    @Override
    protected void doHealthCheck(Health.Builder builder) throws Exception {
        builder.up().withDetail("version", getVersion());
    }

    private String getVersion() {
        return this.rabbitTemplate
                .execute((channel) -> channel.getConnection().getServerProperties().get("version").toString());
    }

}
```

#### 指标监控

```java
public class RabbitMetrics implements MeterBinder {

    private final Iterable<Tag> tags;

    private final ConnectionFactory connectionFactory;

    /**
     * Create a new meter binder recording the specified {@link ConnectionFactory}.
     * @param connectionFactory the {@link ConnectionFactory} to instrument
     * @param tags tags to apply to all recorded metrics
     */
    public RabbitMetrics(ConnectionFactory connectionFactory, Iterable<Tag> tags) {
        Assert.notNull(connectionFactory, "ConnectionFactory must not be null");
        this.connectionFactory = connectionFactory;
        this.tags = (tags != null) ? tags : Collections.emptyList();
    }

    @Override
    public void bindTo(MeterRegistry registry) {
        this.connectionFactory.setMetricsCollector(new MicrometerMetricsCollector(registry, "rabbitmq", this.tags));
    }

}
```

```text
MetricsCollector => AbstractMetricsCollector
                                    => MicrometerMetricsCollector
                                    => NoOpMetricsCollector
                                    => StandardMetricsCollector
```
