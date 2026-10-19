# W4 实验记录（2026-10-19）

## 来源与完成范围
代码、测试与以下记录由 Codex 协助编写；测试输出由 Agent 在原 WSL 仓库实际执行，不冒充学生本人操作或个人经历。已按教师指南先写测试、验证 reference/direct/shallow，再实现函数。W2/W3 成果保留，教师 examples.py、conftest.py 和 test_acceptance.py 未修改。

## 调用前的预测与依据
自选输入：{"seed": 17, "sample_sizes": [240, 1200, 6000, 18000]}。
调用参数：seed=2031，index=1，replacement=3600。
按规则只更新 seed 与第 2 项，预期返回 {"seed": 2031, "sample_sizes": [240, 3600, 6000, 18000]}；原配置仍保持原值。两次调用的结果应 ==，但字典及列表分别 is not；返回对象也分别与 source 的两层容器 is not。测试里的原值与答案由规格独立写出，不从被测函数生成，不使用 before = source。

## 实际核验
在 ~/course/w02-workbench/week-04 执行以下命令，完整输出见 evidence/。

| 命令（前缀 uv run --locked pytest -q） | 实际结果 |
| --- | --- |
| tests/test_student.py --impl=reference | 6 passed |
| tests/test_student.py --impl=direct | 5 failed, 1 passed |
| tests/test_student.py --impl=shallow | 5 failed, 1 passed |
| tests/test_student.py --impl=student | 6 passed |
| tests/test_acceptance.py --impl=student | 24 passed |

两种故障的失败均是断言失败，不是导入或环境错误。

## 一条失败断言与被证据推翻的解释
可检验的错误解释是：“source.copy() 已建立新字典，所以修改列表不会影响 source。”这不是学生本人声称过的观点，而是本次用于验证的假设。
shallow 在 test_both_container_identities 中通过 result is not case，却在 result["sample_sizes"] is not case["sample_sizes"] 失败。这里比较返回列表与原列表的身份，独立身份的预期来自第三项验收承诺；实际两者仍是同一个列表，推翻了该解释。test_source_preserved 还观察到原列表第 2 项由 1200 变成 3600。

## 最终关系与源码位置
variant.py 中 source.copy() 建立独立字典；source["sample_sizes"].copy() 建立独立列表并放入新字典。后两条赋值只更新新字典的 seed 与新列表指定位置。列表元素是不可变整数，不需要再复制整数。每次调用都重新复制，因此两份候选彼此独立。
选做反例也已覆盖：参数不变时 direct 可以通过内容比较 first == second == case，仍被身份断言拒绝。“此刻值相等”不能证明“以后可独立维护”。

## 尚需学生本人完成
请阅读上述预测和源码，形成自己的解释；在 Terminal 亲自重跑 student 的两条命令。课程要求的本人核验和个人反思不能由 Agent 的执行记录代替。Notebook 可用于练习，不是额外提交门槛。本次不声称已替学生完成本人操作。
