## 日志

| op_type             |     context     |  target_id |
|---------------------|:---------------:|-----------:|
| visit               | 路由地址          |            |
| visit_err           | 路由地址          |            |
| login_no_user       | phone_or_email  |            |
| login_fail	      | phone_or_email  |            |
| login_ok	          | phone_or_email: 姓名 |        |
| logout | |
| register            | 邮箱, 手机号, 姓名 |            |
| change_user_profile | 姓名: 字段        | user_id    |
| change_role         | 姓名: 角色        | user_id    |
| reset_password      | 姓名             | user_id    |
| delete_user         | 姓名             | user_id    |
| change_password | |
| change_profile | |

每种操作的含义见 [op_type.py](../controller/op_type.py)
