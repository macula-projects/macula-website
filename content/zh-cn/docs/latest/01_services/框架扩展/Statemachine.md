---
title: "Macula Boot Starter StateMachine"
linkTitle: "状态机"
weight: 11
source_path: "macula-boot-starters/macula-boot-starter-statemachine/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-statemachine/README.md"]
source_branch: "main"
source_commit: "3fbd28dc74d683055d27b81929971c0e45047878"
manual_content: true
---

## 概览

基于[Alibaba COLA Statemachine](https://github.com/alibaba/COLA/tree/master/cola-components/cola-component-statemachine)
的状态机模块，cola statemachine是简单、轻量、性能极高的状态机DSL实现，解决业务中的状态流转问题。

## 组件坐标

下列坐标以继承 [Macula Boot Parent](/docs/latest/00_introduce/概述/#依赖基线) 为前提，由 Parent 管理版本；无需重复声明版本。独立接入时按该节显式定义版本和依赖管理。

```xml

<dependency>
    <groupId>dev.macula.boot</groupId>
    <artifactId>macula-boot-starter-statemachine</artifactId>
</dependency>
```

## 使用配置

状态流转通过 Java DSL 定义，无独立 YAML 配置项。业务负责状态持久化、事务与并发控制，规则定义见“核心功能”。

## 核心功能

本模块仅封装 COLA 状态机依赖，无 YAML 属性或自动持久化能力。规则通过 Java DSL 定义；业务状态的保存、事务和并发控制由应用负责。

### COLA状态机介绍

COLA状态机是在Github开源的，作者也写了介绍文章：https://blog.csdn.net/significantfrank/article/details/104996419。

COLA 使用 Java DSL 声明状态、事件、条件与动作，适用于以明确状态流转为主的业务。状态机定义本身无状态，可复用同一份规则；业务实体的当前状态、持久化与并发控制由应用管理。

其设计侧重简洁的状态流转，不提供嵌套、并行等全部高级状态机能力。选择时应结合业务需要，不能仅凭状态机定义无状态就认定业务动作可以任意并发执行。

COLA 状态机的核心概念包括：

- State：状态

- Event：事件，状态由事件触发，引起变化

- Transition：流转，表示从一个状态到另一个状态

    - External Transition：外部流转，两个不同状态之间的流转
    - Internal Transition：内部流转，同一个状态之间的流转

- Condition：条件，表示是否允许到达某个状态

- Action：动作，到达某个状态之后，可以做什么

- StateMachine：状态机

事件触发转换，经 Condition 判断后执行 Action，得到目标 State。

### COLA状态机实战

首先配置状态机：

```java
/**
 * 状态机初始化
 */
@Configuration
public class LeaveStateMachineConfig {
    private static final Logger logger = LoggerFactory.getLogger(StateMachineRegist.class);
    private final String STATE_MACHINE_ID = "leaveStateMachineId";

    /**
     * 构建状态机实例
     */
    @Bean(name = STATE_MACHINE_ID)
    public StateMachine<ApplyStatusEnum, Event, LeaveContext> stateMachine() {
        StateMachineBuilder<ApplyStatusEnum, Event, LeaveContext> stateMachineBuilder =
            StateMachineBuilderFactory.create();
        // 员工请假触发事件
        // 因为没有源状态，初始化时只是同一个状态流转;所以用内部流转
        stateMachineBuilder.internalTransition().within(ApplyStatusEnum.LEAVE_SUBMIT).on(Event.EMPLOYEE_SUBMIT)
            .perform(doAction());

        // 部门主管审批触发事件（依赖上一个状态：LEAVE_SUBMIT）
        stateMachineBuilder.externalTransition().from(ApplyStatusEnum.LEAVE_SUBMIT).to(ApplyStatusEnum.LEADE_AUDIT_PASS)
            .on(Event.DIRECTLEADER_AUDIT).when(checkIfPass()).perform(doAction());
        stateMachineBuilder.externalTransition().from(ApplyStatusEnum.LEAVE_SUBMIT)
            .to(ApplyStatusEnum.LEADE_AUDIT_REFUSE).on(Event.DIRECTLEADER_AUDIT).when(checkIfNotPass())
            .perform(doAction());

        // hr事件触发(依赖上一个状态:LEADE_AUDIT_PASS)
        stateMachineBuilder.externalTransition().from(ApplyStatusEnum.LEADE_AUDIT_PASS).to(ApplyStatusEnum.HR_PASS)
            .on(Event.HR_AUDIT).when(checkIfPass()).perform(doAction());
        stateMachineBuilder.externalTransition().from(ApplyStatusEnum.LEADE_AUDIT_PASS).to(ApplyStatusEnum.HR_REFUSE)
            .on(Event.HR_AUDIT).when(checkIfNotPass()).perform(doAction());

        return stateMachineBuilder.build(STATE_MACHINE_ID);
    }

    private Condition<LeaveContext> checkIfPass() {
        return (ctx) -> ctx.getIdea().equals(0);
    }

    private Condition<LeaveContext> checkIfNotPass() {
        return (ctx) -> ctx.getIdea().equals(1);
    }

    /**
     * 事件触发后，匹配成功对应的条件后，就会执行具体动作<br>
     * 可以自定义完成具体业务逻辑...
     * @return
     */
    private Action<ApplyStatusEnum, Event, LeaveContext> doAction() {
        return (from, to, event, ctx) -> {
            logger.info("from:" + from + " to:" + to + " on:" + event + " condition:" + ctx);
        };
    }
}
```

然后在需要更改状态的地方，获取状态机实例，触发事件，获取更改后的状态：

```java
public class OrderService {
    @Autowired
    @Qualifier("leaveStateMachineId")
    StateMachine<OrderStatusEnum, OrderEvent, Order> orderOperaMachine;

    public void payOrder(Order order) {
        OrderStatus status = orderOperaMachine.fireEvent(order.status, Events.EVENT1, new Context());
        // 更新订单状态
    }
}
```

具体可以参考[cola-statemachine实践](https://lensman.com.cn/2023/03/14/hdqzkbp1ywg1gt1w/)

## 依赖引入

```xml

<dependencies>
    <dependency>
        <groupId>com.alibaba.cola</groupId>
        <artifactId>cola-component-statemachine</artifactId>
    </dependency>
</dependencies>
```

## 版权说明

- cola-component-statemachine：https://github.com/alibaba/COLA/blob/master/LICENSE
