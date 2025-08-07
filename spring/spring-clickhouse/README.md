## clickhouse客户端

clickhouse客户端底层使用的是http协议，但是交互层遵循jdbc的接口。因此可以作为数据源整合到mybatis-plus中

### 数据源创建器

```java
package com.soyokra.sprival.config.clickhouse;

import com.baomidou.dynamic.datasource.creator.AbstractDataSourceCreator;
import com.baomidou.dynamic.datasource.creator.DataSourceCreator;
import com.baomidou.dynamic.datasource.spring.boot.autoconfigure.DataSourceProperty;
import org.springframework.beans.factory.InitializingBean;
import ru.yandex.clickhouse.ClickHouseDataSource;
import ru.yandex.clickhouse.settings.ClickHouseProperties;

import javax.sql.DataSource;

public class ClickHouseDataSourceCreator extends AbstractDataSourceCreator implements DataSourceCreator, InitializingBean {

  private final SprivalClickHouseProperties clickHouseProperties;

  public static final String CLICK_HOUSE_DATASOURCE = "ru.yandex.clickhouse.ClickHouseDataSource";

  public ClickHouseDataSourceCreator(SprivalClickHouseProperties clickHouseProperties) {
    this.clickHouseProperties = clickHouseProperties;
  }

  @Override
  public DataSource doCreateDataSource(DataSourceProperty dataSourceProperty) {
    ClickHouseProperties clickHouseProperties = new ClickHouseProperties();
    clickHouseProperties.setUser(dataSourceProperty.getUsername());
    clickHouseProperties.setPassword(dataSourceProperty.getPassword());
    clickHouseProperties.setDatabase(this.clickHouseProperties.getDatabase());
    return new ClickHouseDataSource(dataSourceProperty.getUrl(), clickHouseProperties);
  }

  @Override
  public boolean support(DataSourceProperty dataSourceProperty) {
    Class<? extends DataSource> type = dataSourceProperty.getType();
    return CLICK_HOUSE_DATASOURCE.equals(type.getName());
  }

  //  Spring 容器完成对 Bean 的属性设置之后调用
  @Override
  public void afterPropertiesSet() throws Exception {

  }
}
```

### 数据源创建器自动装配

```java
package com.soyokra.sprival.config.clickhouse;

import com.baomidou.dynamic.datasource.spring.boot.autoconfigure.DynamicDataSourceCreatorAutoConfiguration;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import ru.yandex.clickhouse.ClickHouseDataSource;


@Configuration
public class ClickHouseDataSourceCreatorAutoConfiguration {
  @ConditionalOnClass(ClickHouseDataSource.class)
  @Configuration
  static class ClickHouseDataSourceCreatorConfiguration {
    @Bean
    @Order(DynamicDataSourceCreatorAutoConfiguration.DEFAULT_ORDER - 1)
    public SprivalClickHouseDataSourceCreator clickHouseDataSourceCreator(SprivalClickHouseProperties clickHouseProperties) {
      return new SprivalClickHouseDataSourceCreator(clickHouseProperties);
    }
  }
}
```

### 自定义配置类

```java
package com.soyokra.sprival.config.clickhouse;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@Data
@ConfigurationProperties(prefix = "spring.clickhouse")
public class ClickHouseProperties {
    private String database;
}
```

### Java类型映射参考

clickhouse数据类型相比数据库有多不同，以下是映射类型的参考

#### Int | UInt

- Int8 => byte
- Int16 => short
- Int32 => int
- Int64 => long
- Int128 => String
- Int256 => String
- UInt8 => short
- UInt16 => int
- UInt32 => long
- UInt64 => String
- UInt128 => String
- UInt256 => String

#### Float32 | Float64 | BFloat16

- Float32 => float|String

- Float64 => double|String

- BFloat16 => String
  
  > ClickHouse的浮点型有NaN 和 Inf这样的表达方式，如果有使用到这种的话，只能用字符串表示

#### Decimal

Decimal32 => BigDecimal
Decimal64 => BigDecimal
Decimal128 => BigDecimal
Decimal256 => BigDecimal

#### String

String => String
FixedString => String

#### Date

Date32 => Date | Time
DateTime => Date | Time
DateTime64 => Date | Time

#### Enum

Enum => String

#### Bool

Bool => bool

#### UUID

UUID => Sting