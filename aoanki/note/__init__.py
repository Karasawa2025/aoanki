"""
| 字段名     | 类型      | 含义                     |
| ------- | ------- | ---------------------- |
| `id`    | INTEGER | Note ID（主键）            |
| `guid`  | TEXT    | 全局唯一 ID（用于同步）          |
| `mid`   | INTEGER | 模型 ID（Model ID，对应字段数量） |
| `flds`  | TEXT    | 所有字段内容，使用 `\x1f` 分隔    |
| `sfld`  | TEXT    | 搜索字段，通常是第一个字段          |
| `tags`  | TEXT    | 空格分隔的标签字符串             |
| `mod`   | INTEGER | 修改时间戳（ms）              |
| `usn`   | INTEGER | 同步编号                   |
| `csum`  | INTEGER | `sfld` 的校验和（用于去重）      |
| `flags` | INTEGER | 标记状态（星标等）              |
| `data`  | TEXT    | 备用字段                   |

"""
class Note:
    id : int
    guid : str
    note_type : int
    mtime_secs : int
    usn : int
    tags : list[str]
    fields : list[str]