# spring-http-client

spring http client 通常包括以下几个组件

- 负责处理请求响应的http客户端，例如jdk自带的HttpURLConnection，Apache HttpClient，OkHttpClient
- 熔断器，例如hystrix，resilience4j-circuitbreaker，Spring Cloud CircuitBreaker, sentinel
- 重试器，例如Resilience4j-retry
- 负载均衡器，例如Ribbon，load-balance

Retrofit 和 Feign两个声明式http客户端集成了相关的组件

## OkHttp
    
## 监控

