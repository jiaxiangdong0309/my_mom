/**
 * 记忆建议数据生成器
 * 提供高质量的技术知识建议：3种排序算法 + 5种Java设计模式
 * 全部展示，不进行随机选择
 */

// 高质量的建议数据：排序算法
const sortingAlgorithms = [
  {
    title: '快速排序算法 (Quick Sort)',
    content: `快速排序是一种高效的排序算法，采用分治思想。

核心思想：
- 选择一个基准元素（pivot）
- 将数组分为两部分：小于基准的放在左边，大于基准的放在右边
- 递归地对左右两部分进行排序

时间复杂度：
- 平均情况：O(n log n)
- 最坏情况：O(n²)
- 最好情况：O(n log n)

空间复杂度：O(log n)

适用场景：数据量大、随机分布的数据，是实际应用中最常用的排序算法之一。`,
    tags: ['算法', '排序', '数据结构', '快速排序']
  },
  {
    title: '归并排序算法 (Merge Sort)',
    content: `归并排序是一种稳定的排序算法，采用分治和递归思想。

核心思想：
- 将数组不断二分，直到每个子数组只有一个元素
- 然后两两合并有序子数组，直到整个数组有序

时间复杂度：
- 平均情况：O(n log n)
- 最坏情况：O(n log n)
- 最好情况：O(n log n)

空间复杂度：O(n)

优点：
- 时间复杂度稳定，不受数据分布影响
- 稳定排序，相同元素的相对位置不变
- 适合链表排序

适用场景：需要稳定排序、对时间复杂度要求严格的场景。`,
    tags: ['算法', '排序', '数据结构', '归并排序']
  },
  {
    title: '堆排序算法 (Heap Sort)',
    content: `堆排序是一种基于二叉堆数据结构的排序算法。

核心思想：
- 将数组构建成最大堆（或最小堆）
- 将堆顶元素（最大值）与末尾元素交换
- 重新调整堆结构，重复上述过程

时间复杂度：
- 平均情况：O(n log n)
- 最坏情况：O(n log n)
- 最好情况：O(n log n)

空间复杂度：O(1)

优点：
- 时间复杂度稳定
- 原地排序，空间复杂度低
- 适合找出前k个最大/最小元素

适用场景：需要原地排序、对空间复杂度有要求的场景。`,
    tags: ['算法', '排序', '数据结构', '堆排序']
  }
]

// 高质量的建议数据：Java设计模式
const javaDesignPatterns = [
  {
    title: '单例模式 (Singleton Pattern)',
    content: `单例模式确保一个类只有一个实例，并提供一个全局访问点。

实现方式：
1. 饿汉式：类加载时就创建实例
2. 懒汉式：第一次使用时创建实例
3. 双重检查锁定（DCL）
4. 静态内部类
5. 枚举（推荐）

应用场景：
- 数据库连接池
- 线程池
- 配置管理器
- 日志记录器

注意事项：
- 多线程环境下的线程安全
- 序列化/反序列化问题
- 反射攻击防护

示例代码结构：
\`\`\`java
public class Singleton {
    private static volatile Singleton instance;
    private Singleton() {}
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
\`\`\``,
    tags: ['Java', '设计模式', '单例模式', '创建型模式']
  },
  {
    title: '工厂模式 (Factory Pattern)',
    content: `工厂模式提供了一种创建对象的最佳方式，不直接暴露创建逻辑。

类型：
1. 简单工厂模式：一个工厂类根据参数创建不同对象
2. 工厂方法模式：每个产品对应一个工厂类
3. 抽象工厂模式：创建一系列相关或依赖的对象族

优点：
- 解耦：将对象的创建和使用分离
- 扩展性好：新增产品类型只需添加新的工厂类
- 符合开闭原则

应用场景：
- 需要根据配置或参数创建不同类型的对象
- 对象创建过程复杂
- 需要统一管理对象的创建

示例场景：
- 数据库连接工厂（MySQL、PostgreSQL、Oracle）
- 日志记录器工厂（File、Console、Database）
- UI组件工厂（Button、Input、Select）`,
    tags: ['Java', '设计模式', '工厂模式', '创建型模式']
  },
  {
    title: '观察者模式 (Observer Pattern)',
    content: `观察者模式定义对象间一对多的依赖关系，当一个对象状态改变时，所有依赖它的对象都会得到通知。

核心角色：
- Subject（主题）：被观察的对象
- Observer（观察者）：观察主题的对象

实现方式：
1. 推模式：主题主动推送数据给观察者
2. 拉模式：观察者主动从主题拉取数据

Java内置支持：
- java.util.Observable（已废弃）
- java.util.Observer（已废弃）
- 推荐使用自定义实现或事件总线

应用场景：
- 事件驱动系统
- MVC架构中的模型-视图通信
- 发布-订阅系统
- GUI事件处理

优点：
- 松耦合：主题和观察者之间抽象耦合
- 支持广播通信
- 符合开闭原则

注意事项：
- 观察者过多时可能影响性能
- 循环依赖问题`,
    tags: ['Java', '设计模式', '观察者模式', '行为型模式']
  },
  {
    title: '策略模式 (Strategy Pattern)',
    content: `策略模式定义一系列算法，把它们封装起来，并使它们可以互换。

核心思想：
- 将算法封装成独立的策略类
- 客户端可以选择使用哪种策略
- 策略之间可以相互替换

结构：
- Context（上下文）：使用策略的类
- Strategy（策略接口）：定义算法接口
- ConcreteStrategy（具体策略）：实现具体算法

应用场景：
- 多种支付方式（支付宝、微信、银行卡）
- 多种排序算法（快速排序、归并排序、堆排序）
- 多种数据验证规则
- 多种折扣计算方式

优点：
- 算法可以自由切换
- 避免使用多重条件判断
- 扩展性好，新增策略容易
- 符合开闭原则

示例代码结构：
\`\`\`java
interface PaymentStrategy {
    void pay(double amount);
}
class AlipayStrategy implements PaymentStrategy { ... }
class WechatStrategy implements PaymentStrategy { ... }
class PaymentContext {
    private PaymentStrategy strategy;
    public void setStrategy(PaymentStrategy strategy) { ... }
    public void executePayment(double amount) { ... }
}
\`\`\``,
    tags: ['Java', '设计模式', '策略模式', '行为型模式']
  },
  {
    title: '装饰器模式 (Decorator Pattern)',
    content: `装饰器模式动态地给对象添加额外的职责，比继承更灵活。

核心思想：
- 不改变原有对象结构
- 通过组合的方式扩展功能
- 可以动态地添加或移除功能

结构：
- Component（组件接口）：定义对象的接口
- ConcreteComponent（具体组件）：被装饰的对象
- Decorator（装饰器）：持有组件引用，实现组件接口
- ConcreteDecorator（具体装饰器）：添加具体功能

Java中的应用：
- java.io包中的流处理（BufferedInputStream、DataInputStream等）
- Java I/O就是装饰器模式的典型应用

应用场景：
- 需要动态、透明地给对象添加职责
- 需要撤销职责
- 用继承扩展功能不现实时

优点：
- 比继承更灵活
- 可以动态组合功能
- 符合开闭原则
- 可以任意组合装饰器

缺点：
- 会产生很多小对象
- 代码复杂度增加

示例场景：
- 咖啡加糖、加奶、加巧克力
- 文本编辑器添加粗体、斜体、下划线
- 数据流添加缓冲、压缩、加密功能`,
    tags: ['Java', '设计模式', '装饰器模式', '结构型模式']
  }
]

/**
 * 随机选择一个数组元素
 */
function randomChoice(array) {
  return array[Math.floor(Math.random() * array.length)]
}

/**
 * 随机选择多个不重复的元素
 */
function randomChoices(array, count) {
  const shuffled = [...array].sort(() => 0.5 - Math.random())
  return shuffled.slice(0, Math.min(count, array.length))
}

/**
 * 生成一条随机记忆建议（保留原有功能，用于向后兼容）
 */
export function generateRandomSuggestion() {
  // 合并所有高质量建议
  const allSuggestions = [...sortingAlgorithms, ...javaDesignPatterns]
  return randomChoice(allSuggestions)
}

/**
 * 生成所有记忆建议（全部展示，不随机）
 * @param {number} count 参数保留用于向后兼容，但会忽略，返回全部建议
 */
export function generateRandomSuggestions(count = 3) {
  // 合并所有高质量建议：先排序算法，后设计模式
  const allSuggestions = [...sortingAlgorithms, ...javaDesignPatterns]

  // 返回全部建议，不进行随机选择
  return allSuggestions
}

