# mybatis Mapper接口实现原理

mybatis通过JDK动态代理把mapper接口面向业务的方法通过转换为操作数据库的方法

## 类关系图
```
MapperRegistry -> MapperProxyFactory -> MapperProxy -> MapperMethod
```
- MapperRegistry：MapperProxyFactory的注册缓存
- MapperProxyFactory：创建MapperProxy实例
- MapperProxy：动态代理Mapper接口
- MapperMethod：将Mapper面向业务的方法转换为操作数据库的方法

##  JDK动态代理

此处为示例代码，用于演示实现原理，方面理解：

### 接口
```
public interface UserMapper {
    String queryUser(String id);
}
```

### 代理
```
public class MapperProxy implements InvocationHandler {
     @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        // 转为操作mysql的select,update,delete等方法
    }
}
```

### 生成动态代理对象
```
UserMapper userMapper = (UserMapper) Proxy.newProxyInstance(UserMapper.class.getClassLoader(), new Class[] { UserMapper.class }, mapperProxy);
userMapper.queryUser("10028301010"); // 实际调用 MapperProxy.invoke 方法。
```

