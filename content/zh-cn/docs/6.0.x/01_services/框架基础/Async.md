---
title: "Macula Boot Starter Async"
linkTitle: "Async"
weight: 0
source_path: "macula-boot-starters/macula-boot-starter-async/README.md"
source_paths: ["macula-boot-starters/macula-boot-starter-async/README.md"]
source_branch: "6.0.x"
source_commit: "fbd20cfd4020734880ff4cc41f7cec95a0bfd70e"
---

# Macula Boot Starter Async

## @Aysnc注解支持TTL

```java
public class AsyncAutoConfiguration {
    @Bean
    public TaskDecorator ttlTaskDecorator() {
        return TtlRunnable::get;
    }
}
```

## CompletableFuture支持TTL

```java
CompletableFuture;CompletableFuture.runAsync(TtlRunnable.get(() -> {
    //... do your business
}));

CompletableFuture.supplyAsync(TtlWrappers.wrapSupplier(() -> {
    //... do your business
}));

// 建议采用下述方式与@Async共享Executor
CompletableFuture.runAsync(()-> {
        //... do your business
}), taskExecutor);
```
