"""
| 字段名     | 类型      | 含义                                            |
| ------- | ------- | --------------------------------------------- |
| `id`    | INTEGER | 卡片唯一 ID（通常是时间戳）                               |
| `nid`   | INTEGER | 所属 note 的 ID（外键）                              |
| `did`   | INTEGER | 所属牌组 deck 的 ID                                |
| `ord`   | INTEGER | 模板编号（0 表正面卡，1 表背面卡）                           |
| `queue` | INTEGER | 队列（-1=suspended, 0=new, 1=learn, 2=review）    |
| `type`  | INTEGER | 卡片类型（0=new, 1=learn, 2=review, 3=relearn）     |
| `due`   | INTEGER | 到期时间（视 queue 类型而定）                            |
| `ivl`   | INTEGER | 间隔天数                                          |
| `mod`   | INTEGER | 上次修改时间戳（ms）                                   |
| `usn`   | INTEGER | 同步用标识                                         |
| 其他字段    |         | 如 `factor`, `reps`, `lapses`, `flags`, `data` |

"""