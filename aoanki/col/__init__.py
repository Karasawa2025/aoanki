"""
| 字段名      | 类型      | 含义                   |
| -------- | ------- | -------------------- |
| `id`     | INTEGER | 恒为 1（主键）             |
| `crt`    | INTEGER | 创建时间戳                |
| `mod`    | INTEGER | 最后修改时间戳              |
| `scm`    | INTEGER | 模板同步时间戳              |
| `ver`    | INTEGER | 版本号                  |
| `dty`    | INTEGER | 是否 dirty（修改后未同步）     |
| `usn`    | INTEGER | 同步编号                 |
| `ls`     | INTEGER | 上次同步时间               |
| `conf`   | TEXT    | 配置 JSON（默认设置）        |
| `models` | TEXT    | 模板 JSON（字段、模板结构）     |
| `decks`  | TEXT    | 牌组 JSON（deck 名、复习计数） |
| `dconf`  | TEXT    | 复习设置 JSON（如间隔、步骤）    |
| `tags`   | TEXT    | 标签使用统计 JSON          |

"""