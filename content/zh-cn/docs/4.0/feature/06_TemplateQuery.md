---
aliases: ["/docs/98_old/v4.0/feature/06_templatequery/", "/docs/5.x/98_old/v4.0/feature/06_templatequery/", "/docs/6.0.x/98_old/v4.0/feature/06_templatequery/", "/docs/latest/98_old/v4.0/feature/06_templatequery/", "/docs/v4.0/feature/06_templatequery/"]
type: docs
title: "TemplateQuery"
linkTitle: "TemplateQuery"
weight: 1
description: ""
---
Macula扩展了spring-data-jpa的功能，除了原先可以支持的@Query、@NamedQuery等方法上的注解，Macula提供了TemplateQuery注解。

原先的注解SQL语句不支持动态条件，不能写if等表达式。TemplateQuery注解支持在注解中或者模板文件中编写SQL语句，可以使用freemarker语法编写，具体使用方式如下：

```java
package org.macula.core.test.repository;
...
public UserRepository extends MaculaJpaRepository<User> {
    ...
    @TemplateQuery
    public Page<UserVo> findByLastNameVo(@Param("lastName") String lastName, Pageable pageable);
   
    @TemplateQuery
    public Page<User> findByLastNameMap(@Param("data") Map<String, Object> data, Pageable pageable);
   
     @TemplateQuery("select * from MY_USER u where 1=1" +
           "<#if (data.lastName)??>" +
          "    and u.last_name = :data.lastName" + 
          "</#if>" +
          "<#if firstNames??>" +
          "    and u.first_name in (:firstNames)" +
          "</#if>")
    public Page<User> findByLastNameMapAndList(@Param("data") Map<String, Object> data, 
                    @Param("firstNames") List<String> firstNames, Pageable pageable);
    
    @TemplateQuery
    public Page<User> findByLastNameMapAndListx(@Param("data") Map<String, Object> data, 
                    @Param("firstNames") List<String> firstNames, Pageable pageable);
    
    @TemplateQuery
    public Page<User> findByLastNameMapy(@Param("data") Map<String, Object> data, Pageable pageable);
    
    @TemplateQuery
    public Page<User> findByLastNameMapAndListy(@Param("data") Map<String, Object> data, 
                    @Param("firstNames") List<String> firstNames, Pageable pageable);
}
```
同时，没有在@TemplateQuery value中写的SQL需要在文件中编写对应的SQL模板：

xml格式模板

xml中编写SQL，文件放在该TemplateQuery方法所属的Repository类路径下，和Repository类名称一致，以xml结尾。例如：src/java/org/macula/core/test/repository/UserRepository.xml

```xml
<?xml version="1.0" encoding="utf-8" ?>
<sqls xmlns="http://www.maculaframework.org/schema/repository"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.maculaframework.org/schema/repository http://macula.top/schema/repository/macula-repository-1.0.xsd">
    <sql name="findByLastNameVo">
        <![CDATA[
          select u.first_name, u.last_name from MY_USER u where u.last_name = :lastName
        ]]>
    </sql>
    <sql name="findByLastNameMap">
        <![CDATA[
          select * from MY_USER u where u.last_name = :data.lastName
        ]]>
    </sql>
    <sql name="findByLastNameMapAndListx">
        <![CDATA[
          select * from MY_USER u where 1=1
           <#if (data.lastName)??>
              and u.last_name = :data.lastName 
          </#if>
          <#if firstNames??>
              and u.first_name in (:firstNames)
          </#if>
        ]]>
    </sql>
</sqls>
```

2.sftl格式模板

具体放置路径同XML模板，只是把后缀改为.sftl：

```xml
--findByLastNameMapy
    select * from MY_USER u where u.last_name = :data.lastName
--findByLastNameMapAndListy
    select * from MY_USER u where 1=1
    <#if (data.lastName)??>
      and u.last_name = :data.lastName 
    </#if>
    <#if firstNames??>
      and u.first_name in (:firstNames)
    </#if>
```

### TemplateQuery使用优先级

TemplateQuery支持通过注解、文件、配置属性提供SQL，如果出现RepositoryName加MethodName重复，则配置属性优先，注解次之，文件中的SQL最后。


### 使用通用配置热修复TemplateQuery的SQL

线上运行的系统有时发现TemplateQuery的SQL写得有问题，可以通过Macula支持的基于zookeeper和Nacos的通用配置临时添加一个属性热修复。具体属性KEY是macula.templateQuery.{repositoryName}.{methodName}，内容是SQL模板。请谨慎使用，待程序修复后要即时删除该配置，否则永远是这个配置优先。

