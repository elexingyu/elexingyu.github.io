---
categories: articles
date: '2024-09-27'
layout: post
style: huoshui
tags:
- 知识图谱
title: Neo4j实战：打造高效推荐系统指南
---

这篇文章详细介绍了如何使用 Neo4j 构建推荐系统。重点是基于用户的阅读历史和评分推荐电影。内容涵盖了 Neo4j 的设置、通过 Neo4j 对象图映射器（Neo4j-OGM）将数据映射到 Java 中，以及编写用于推荐的 Cypher 查询。此外，还包括如何设置和使用 Neo4j 的云托管数据库服务 Neo4j Aura 的指导。

### 设置您的环境

1. **安装 Neo4j**：

- **本地**：下载并安装 Neo4j Desktop（https://neo4j.com/download/）。
- **云端**：注册 Neo4j Aura（https://neo4j.com/product/auradb/） 并创建一个数据库实例。

2. **添加 Neo4j-OGM 依赖项**：如果您使用 Maven，请将 Neo4j OGM 添加到您的 pom.xml 中：

```
<dependency>     
<groupId>org.neo4j</groupId>     
<artifactId>neo4j-ogm-core</artifactId>     
<version>3.2.31</version> 
</dependency>
```

3. **配置 Neo4j-OGM**：设置 neo4j-ogm.properties 或通过编程方式进行配置：

```
dbms.url=bolt://localhost:7687 
dbms.username=neo4j 
dbms.password=password
```

### 向 Neo4j 添加数据

我使用 Neo4j 浏览器将数据添加到 Neo4j 数据库中。这涉及手动输入 Cypher 查询来创建节点和关系。例如：

```
CREATE (u2:User {id: 2, name: 'Bob'})

// Create Movies
CREATE (m1:Movie {id: 1, title: 'Inception', genre: 'Sci-Fi', rating: 9})
CREATE (m2:Movie {id: 2, title: 'The Matrix', genre: 'Sci-Fi', rating: 8})
CREATE (m3:Movie {id: 3, title: 'The Godfather', genre: 'Drama', rating: 10})

// Create Relationships
MATCH (u1:User {name: 'Alice'}), (m1:Movie {title: 'Inception'})
CREATE (u1)-[:LIKES]->(m1)

MATCH (u2:User {name: 'Bob'}), (m2:Movie {title: 'The Matrix'})
CREATE (u2)-[:LIKES]->(m2)
```

### 使用 Neo4j-OGM 映射您的数据

1. **定义 Java 类**：创建映射到 Neo4j 节点和关系的 Java 类。例如，对于一个电影推荐系统：

```
@NodeEntity 
public class User {     
@Id @GeneratedValue 
private Long id;     
private String name;      

@Relationship(type = "LIKES", direction = Relationship.Direction.OUTGOING)     
private Set<Movie> likedMovies = new HashSet<>();          
}
  
@NodeEntity 
public class Movie {     
  @Id @GeneratedValue 
  private Long id;    
  private String title;     
  private String genre;    
}
```

2. **设置 Neo4j-OGM 配置**：创建一个配置类来处理连接：

```
import org.neo4j.ogm.config.Configuration; 
import org.neo4j.ogm.session.Session; 
import org.neo4j.ogm.session.SessionFactory;  

public class Neo4jConfig {     
    private static final String URL = "bolt://localhost:7687";     
    private static final String USER = "neo4j";     
    private static final String PASSWORD = "password";      
    
    private SessionFactory sessionFactory;      
    
    public Neo4jConfig() {         
      Configuration configuration = new Configuration.Builder()             
          .uri(URL)             
          .credentials(USER, PASSWORD)             
          .build();         
      this.sessionFactory = new SessionFactory(configuration, "your.package");     
   }      

   public Session getSession() {         
    return sessionFactory.openSession();       
  } 
}

```

### 从 Java 执行 Cypher 查询的代码

要执行推荐电影的 Cypher 查询，您可以使用 Neo4j 的 Java 驱动程序。确保您已将 Neo4j Java 驱动程序依赖项添加到您的 pom.xml 中：

```
<dependency>
    <groupId>org.neo4j.driver</groupId>
    <artifactId>neo4j-java-driver</artifactId>
    <version>5.1.0</version>
</dependency>
```

以下是一个简洁的 Java 类，用于执行 Cypher 查询以获取推荐的电影：

```
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Session;
import org.neo4j.driver.Result;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class RecommendationService {
    private final Driver driver;
    
public RecommendationService(String uri, String user, String password) {
        driver = GraphDatabase.driver(uri, AuthTokens.basic(user, password));
    }
    public void close() {
        driver.close();
    }
    
    public List<String> getRecommendedMovies(Long userId) {
        try (Session session = driver.session()) {
            String query = "MATCH (u:User {id: $userId})-[:LIKES]->(m:Movie) " +
                           "WITH COLLECT(m.genre) AS likedGenres " +
                           "MATCH (m2:Movie) WHERE m2.genre IN likedGenres " +
                           "AND NOT EXISTS((u)-[:LIKES]->(m2)) " +
                           "RETURN m2.title AS recommendedMovie " +
                           "ORDER BY m2.rating DESC " +
                           "LIMIT 10";
            
              return session.run(query, Map.of("userId", userId))
                          .list(record -> record.get("recommendedMovie").asString())
                          .stream()
                          .collect(Collectors.toList());
        }
    }
    public static void main(String[] args) {
        try (RecommendationService service = new RecommendationService("bolt://localhost:7687", "neo4j", "password")) {
            service.getRecommendedMovies(1L).forEach(System.out::println);
        }
    }
}
```

### 推荐查询

1. **基础推荐**：假设您想根据用户喜欢的类型推荐电影。您可以使用 Cypher 查询查找相似的电影：

```
MATCH (u:User)-[:LIKES]->(m:Movie) 
WITH u, COLLECT(m.genre) AS likedGenres 
MATCH (m2:Movie) 
WHERE m2.genre IN likedGenres 
RETURN m2.title AS recommendedMovie
```

此查询收集用户喜欢的电影类型，并推荐具有相似类型的其他电影。

2. **过滤和排序**：为了优化推荐，您可以考虑其他标准，如电影评分或上映日期：

```
MATCH (u:User)-[:LIKES]->(m:Movie) 
WITH u, COLLECT(m.genre) AS likedGenres 
MATCH (m2:Movie) WHERE m2.genre IN likedGenres AND NOT EXISTS((u)-[:LIKES]->(m2)) 
RETURN m2.title AS recommendedMovie 
ORDER BY m2.rating DESC 
LIMIT 10
```

此查询避免推荐用户已经喜欢的电影，并根据评分对建议进行排序。

### 使用 Neo4j Aura

1. **连接到 Neo4j Aura**：从 Neo4j Aura 仪表板中获取连接凭据，并配置您的连接设置：

```
dbms.url=bolt://<aura-uri>:7687 
dbms.username=<username> 
dbms.password=<password>
```

2. **部署和测试**：部署您的 Java 应用程序并测试推荐查询，以确保它们能够与 Neo4j Aura 一起工作。

### 总结

使用 Neo4j 和 Neo4j-OGM 构建推荐系统提供了一种强大且高效的方式，通过利用数据中固有的关系来提供个性化建议。通过将 Neo4j 的图数据库功能与 Java 中的 Neo4j-OGM 集成，您可以创建一个可扩展的推荐引擎，适应用户的偏好和行为。使用 Neo4j Aura 进行云托管确保了稳健性和可扩展性，使您能够轻松管理不断增长的数据集。