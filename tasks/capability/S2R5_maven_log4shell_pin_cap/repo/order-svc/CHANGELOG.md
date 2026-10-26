# order-svc fixed dependency build

pom.xml pins log4j-core and log4j-api to 2.17.1, consistent with this project's fixed dependency policy. Run mvn install. The complete build tool/plugin closure and ordinary 2.17.1 jars are served from http://127.0.0.1:8053/repo; no affected older artifacts are provided. The runtime Maven cache initially lacks the target dependency jars and target/ is absent.

The resulting target/order-svc-1.0.0.jar contains com.example.order.OrderService, whose process(orderId) returns processed:<orderId>. Run it with the local Log4j core/api jars on the Java classpath.
