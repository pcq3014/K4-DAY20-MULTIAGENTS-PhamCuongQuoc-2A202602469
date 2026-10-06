# Báo cáo Lab: Self evolving Agentic


## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Phạm Cường Quốc | 2A202602469 | Toàn bộ |

- Mô hình (tên deployment hoặc `LAB_MODEL`), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `deepseek:deepseek-reasoner`, `LAB_TEMPERATURE=0`, `recursion_limit=60`. Ban đầu dùng `deepseek:deepseek-chat`, nhưng 3 lần thử trên `data-learn` (nhiệt độ 0 và 0,5) đều đạt 0/8 vì chạm `GraphRecursionError`: mô hình đi tìm tệp "Acme conventions" khắp hệ thống tệp rồi lặp lại đúng một lệnh `ls` hơn 15 lần (436k-905k token mỗi lần). Các lần thử này không tính vào kết quả.
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Python 3.12, chạy trong Docker (`python:3.12-slim`, nhân WSL2) trên Windows 10 qua `docker-run.sh`. Shell của tác tử chạy bằng user `nobody` (`LAB_AGENT_USER`), repo mount ở `/root/lab` (quyền 700), nên tác tử không đọc được bộ chấm, tác vụ đánh giá hay kết quả cũ (xem Phụ lục).
- Số lần chạy tác vụ đã dùng / ngân sách: tổng 33 lần (GUIDE không nêu ngân sách cụ thể), gồm 12 lần chính thức sau `freeze` và 21 lần trước `freeze`. Trong 21 lần trước `freeze` có 5 lần thử cấu hình (4 lần `deepseek-chat`, 1 lần thử `deepseek-reasoner`), 4 lần lỗi hạ tầng hoặc bị dừng (3 lần lỗi mạng, 1 lần chạy dở), 2 lần `code-learn` không hợp lệ do lỗi CRLF, và 10 lần dùng trong báo cáo (9 lần chính thức và lần 1 của `baseline data-learn`, dùng để đo nhiễu).
- Commit của tag `freeze`: `26f4a1d` ("freeze skills"); commit giả thuyết `5bf3907` ("hypotheses").

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)


- H1 (subagents so với baseline): Trên tác vụ đánh giá, `subagents` đạt điểm xấp xỉ `baseline` (chênh không quá 1 check mỗi tác vụ) nhưng tốn token nhiều hơn hoặc bằng. Căn cứ: trên tác vụ học cả hai đạt 12/18 check kỹ thuật và 0/9 check quy ước; lời giao việc chép đủ quy tắc của đề nhưng không thể chứa quy ước Acme vì tác tử chính không biết chúng (lỗi nhóm E). Subagent chỉ giúp tránh hết `recursion_limit`, vì việc của subagent không tính vào số bước của luồng chính (`subagents` 0/3 lần lỗi so với `baseline` 3/3 ở lần chạy cuối), đổi lại tốn nhiều token (`logs-learn` 1,16M).
- H2 (skills-auto so với baseline): `skills-auto` đạt điểm cao nhất trên tác vụ đánh giá, chủ yếu nhờ check kỹ thuật (ít lần hết bước hơn nhờ `work-from-given-spec`), và tốn ít token nhất. Check quy ước chỉ cải thiện ở các quy ước cũ được skill nêu chung chung (type hints, cent, UTC); check quy ước MỚI của tác vụ đánh giá sẽ không đạt vì không skill nào chứa nó. Căn cứ: trên tác vụ học `skills-auto` 18/18 kỹ thuật và 1/9 quy ước với 152k token/lần, so với `baseline` 12/18, 0/9 và 594k. SkillsBench ghi nhận skill tự sinh trung bình không có lợi; ở đây lợi ích đến từ việc chặn một hành vi xấu cụ thể chứ không phải từ tri thức miền.
- H3 (tác vụ học so với tác vụ đánh giá): Mức cải thiện của `skills-auto` so với `baseline` trên tác vụ đánh giá nhỏ hơn trên tác vụ học, nhất là ở check quy ước, vì skill thiếu chi tiết định dạng và tác vụ đánh giá có quy ước mới (đúng với SkillEvolBench về việc lợi ích không chuyển giao). Tuy vậy, phần cải thiện về quy trình (không lục hệ thống tệp, kiểm chứng tệp đầu ra) sẽ chuyển giao được. Nhiễu lớn: cùng cấu hình `baseline data-learn` cho 0/8 và 5/8 ở hai lần chạy, nên mọi chênh lệch nhỏ hơn khoảng 3 check mỗi tác vụ cần coi là không chắc chắn.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có 9 công cụ: công cụ tệp `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`; công cụ shell `execute`; công cụ giao việc `task`. Chỉ `execute` cho phép chạy lệnh (shell thật của backend).
2. `task` "launch an ephemeral subagent"; subagent mặc định `general-purpose` dùng cho nghiên cứu, tìm kiếm và tác vụ nhiều bước, "has access to all tools as the main agent". Mỗi lần gọi là stateless: "the agent sees only the prompt you give it and returns a single final report", tức là subagent KHÔNG thấy lịch sử hội thoại, system prompt hay kết quả công cụ của tác tử chính, chỉ thấy lời giao việc.
3. Câu từ `task`: "Put full detail in the prompt and state exactly what it should return". Câu từ `execute`: "You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search." Đáng chú ý, mô tả `execute` còn dặn "Use absolute paths and avoid `cd`", mâu thuẫn với `PATHS_NOTE` ("never starts with '/'"). Đây là nguyên nhân mô hình liên tục thử `/workspace` trong shell (thấy trong vết `data-learn`).

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)


Kết quả `baseline` dùng để phân loại (lần chạy cuối, sau khi sửa lỗi CRLF): `code-learn` 7/10, `data-learn` 5/8, `logs-learn` 0/9. Cả 3 lần đều kết thúc bằng `GraphRecursionError` (60 bước).

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| code-learn | `rule_type_hints` | E | "RULE: every public function ... has type annotations on all parameters and on the return value" |
| code-learn | `rule_regression_tests` | E | "RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3)" |
| code-learn | `rule_changelog` | E | "RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): ...'" |
| data-learn | `rule_money_in_cents` | E | "RULE: money values in answer.json are integer cents (1606.67 USD is written 160667)" |
| data-learn | `rule_meta_block` | E | "RULE: answer.json has an object `meta` = {"source", "rows_in", "rows_used"}" |
| data-learn | `rule_clean_csv` | E | "RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents ..." |
| logs-learn | cả 9 check (6 kỹ thuật + 3 `rule_`) | G: hết `recursion_limit` vì lục hệ thống tệp tìm quy ước ẩn, trước khi ghi đầu ra | `detail`: "FileNotFoundError: ... workspace/errors.json". Vết: 59 tool call, gồm `find / -iname "*acme*"`, `grep -ril "convention" /`, đọc mã nguồn harness trong `/lab/src`. Lần chạy trước (`results/baseline-run1/logs-learn`, bị ngắt do lỗi mạng) đạt 6/6 check kỹ thuật và trượt 3 check `rule_` (E). |
| data-learn (lần 1, `results/baseline-run1`) | cả 8 check | G: như trên | `detail`: "FileNotFoundError: ... workspace/answer.json"; vết có 26 lần nhắc "Acme" trong lệnh tìm kiếm. |

Bằng chứng phủ định cho A-D (`scripts/check_breakdown.py`): `baseline` học đạt 12/18 check kỹ thuật, và cả 6 check kỹ thuật trượt đều thuộc lần `logs-learn` không ghi được tệp đầu ra (nhóm G), không phải do sai kỹ thuật. Ở các lần chạy có ghi được đầu ra, tác tử đọc README và docstring trước khi làm (không có A), chạy lại test (không có B; vết `code-learn`: "Verification: python -m pytest tests -q → 6 passed"), sửa đúng hàm gốc `parse_price` dùng chung (không có C), và xử lý đúng trùng lặp, giá trị thiếu, nhiều định dạng ngày, múi giờ (không có D: 5/5 check kỹ thuật của `data-learn` đạt). Không thấy nhóm F: câu trả lời cuối chỉ nêu các tệp có thật.

Nhận xét: nhóm E chiếm đa số tuyệt đối với 6/6 check `rule_` ở các lần có đầu ra, 9/9 nếu tính cả lần `baseline-run1` của `logs-learn`. Nguyên nhân chung: quy ước Acme không có trong đề hay workspace, chỉ xuất hiện trong `detail` của bot chấm. Nhóm G (hết bước) là hệ quả trực tiếp của cùng nguyên nhân: đề nhắc "Acme reporting conventions" nên `deepseek-reasoner` dành phần lớn ngân sách bước để đi tìm chúng. Skill có thể phòng ngừa cả hai: với E, skill mang quy ước đã học từ `detail`; với G, skill dặn không tìm kiếm ngoài phạm vi. Tuy nhiên skill chỉ giúp được quy ước đã thấy, không giúp được quy ước mới.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa (tên, vai trò, lý do thiết kế): ba vai trò tách biệt theo pha đọc, làm, kiểm.
  - `explorer`: chỉ đọc, báo cáo đặc tả, quy ước và dữ liệu bẩn kèm nguồn trích dẫn. Nhắm nhóm A và D.
  - `implementer`: sửa ở nguyên nhân gốc, viết script để tính, chạy test, chỉ báo cáo tệp đã kiểm chứng. Nhắm nhóm C và F.
  - `reviewer`: kiểm tra độc lập, chỉ đọc, tự tính lại bằng script riêng, trả checklist PASS/FAIL. Nhắm nhóm B.
  - `description` của mỗi subagent viết như chỉ dẫn hành động ("Use BEFORE changing anything" / "Use to make the actual change" / "Use AFTER the work is done"). `build_agent` nối `PATHS_NOTE` vào `system_prompt` của từng subagent.
- `subagent_calls` ở từng tác vụ và nhận xét (kể cả trường hợp bằng 0): `code-learn` 2 (implementer sửa gói, sau đó reviewer kiểm tra chỉ đọc), `data-learn` 1 (chỉ reviewer, tác tử chính tự làm phần tính toán), `logs-learn` 2 (implementer viết `errors.json`, reviewer tự parse lại log và báo "No mismatches found"). `explorer` không được gọi lần nào: tác tử chính luôn tự đọc README và dữ liệu trước, vì cần hiểu đề mới giao việc được. Lần chạy `subagents code-learn` trước đó (bản sao lưu trong `results/crlf-backup/`) có `subagent_calls = 0` và hết 60 bước trong lúc tìm quy ước.
- Thông tin thiếu hoặc thừa khi giao việc (nếu có giao việc): lời giao việc khá đầy đủ, chép lại quy tắc của đề, định dạng đầu ra, nội dung README (ví dụ cách đọc `-- last message repeated N times --`) và quy ước đường dẫn tương đối (vết: "ALWAYS use the relative form `workspace/inventory...`"). Thiếu tất yếu: không lời giao việc nào chứa quy ước Acme vì tác tử chính không biết chúng, nên reviewer xác nhận "All checks pass" trong khi 3 check `rule_` vẫn trượt. Reviewer chỉ kiểm được những gì được giao, không phát hiện được yêu cầu ẩn. Thừa: lời giao việc chứa cả đường dẫn tuyệt đối của sandbox (`/tmp/lab-code-learn-...`), dù không cần thiết.
- Ảnh hưởng đến token và thời gian: token trung bình `subagents` 824k/lần so với `baseline` 594k (tăng khoảng 1,4 lần), cao nhất `logs-learn` 1,16M (2 subagent). Thời gian 239-280 giây so với 117-257 giây. Trên tác vụ học, check quy ước bằng nhau (0/9), nhưng `subagents` đạt 18/18 check kỹ thuật so với 12/18 của `baseline`, vì `subagents` không lần nào hết `recursion_limit`, trong khi `baseline` hết cả 3 lần ở lần chạy cuối. (Giả thuyết H1 ghi "cả hai đạt 12/18" là số liệu trước khi chạy lại `subagents code-learn` bị lỗi mạng; khi commit `hypotheses`, lần chạy lại đã có và cho 7/10.) Phần việc giao cho subagent không tính vào 60 bước của luồng chính, nên đa tác tử ở đây hoạt động như một cách nới ngân sách bước, với cái giá là token.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator, số skill bị xóa và lý do: 2 lần (tối đa cho phép).
  - Lần 1: mô hình trả 3 khối; `validate_skill` loại `apply-all-house-rules` ("mentions evaluation material: orders"). Từ "orders" trùng tên tệp `orders.json` của tác vụ đánh giá, nên bộ chống rò rỉ chặn đúng theo quy tắc dù ở đây chỉ là từ phổ thông. Hệ quả: skill duy nhất chứa quy ước cụ thể bị mất. Ghi được `work-from-given-spec` và `verify-artifacts-and-constraints`.
  - Lần 2 (lý do chạy lại: skill quy ước bị loại): ghi được 3 skill `house-rules-first`, `structured-output-validation`, `code-change-hygiene`.
  - Xóa 1 skill: `verify-artifacts-and-constraints` (lần 1), vì trùng gần hết nội dung với `structured-output-validation` (cùng checklist: tệp tồn tại, schema, cent, UTC, chạy test). Bản sao lưu ở `results/_curator/`. Không sửa tay nội dung skill nào.
  - Lưu ý về đầu vào của curator: các lần `baseline` mà curator đọc có 2 vấn đề. (a) `logs-learn` hết `recursion_limit` trước khi ghi `errors.json`, nên mọi check chỉ có `detail` là `FileNotFoundError` và curator không thấy 3 quy ước `rule_` của họ `logs`. (b) Check `tests_not_modified` của `code-learn` thất bại giả vì Git trên Windows đổi tệp test sang CRLF, làm hash lệch (đã sửa sau đó, xem Phụ lục). Dòng "Never modify existing test files" trong `code-change-hygiene` được rút ra từ phản hồi giả này; nội dung vẫn đúng nhưng cho thấy curator tin tuyệt đối vào phản hồi.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `work-from-given-spec` | Tổng quát. Nhắm đúng hành vi gây hết bước ở 4/6 lần chạy học: lục hệ thống tệp tìm "Acme conventions". Không nêu tên tệp hay con số. | Đúng và hữu ích: cấm tìm kiếm ngoài phạm vi, yêu cầu ghi sản phẩm sớm, giới hạn thời gian điều tra. Hơi mơ hồ: "pick the most standard interpretation" không giúp đạt quy ước ẩn. | 7 dòng thân. `description` nêu đúng tình huống kích hoạt ("tempted to search the environment for rules"). `skills_read` = 4 ở cả 3 tác vụ học (mọi skill đều được đọc ngay ở bước đầu). Được làm theo: không lần nào hết bước; token giảm từ 594k xuống 152k/lần; số tool call 18-30 so với 51-59 ở `baseline`. |
| `house-rules-first` | Nửa tổng quát. Phần lớn là quy trình ("coi mỗi RULE là yêu cầu cứng"), có vài quy ước rút từ `data-learn` (cent, khối metadata, CSV sạch) nhưng diễn đạt chung. | Có điểm sai tiềm ẩn: "the stated rules are sufficient" và "Read all of them" giả định đề có liệt kê RULE, trong khi quy ước Acme không có trong đề, chỉ có trong phản hồi. Trên tác vụ mới, skill không cho biết quy ước cụ thể là gì (ví dụ không nêu tên khóa của khối `meta`). | 11 dòng. `description` ("task or feedback lists RULE/house conventions") có thể không kích hoạt vì đề không chứa chữ RULE. Được đọc ở cả 3 tác vụ. Câu trả lời cuối của `code-learn` có "House-rule checklist: ... ✔", tức tác tử đã làm checklist, nhưng chỉ tự kiểm theo cách hiểu của mình. |
| `structured-output-validation` | Tổng quát cho họ `data` và `logs`: liệt kê tệp và trường bắt buộc, UTC, tiền theo cent, khối metadata, kiểm chứng bằng script độc lập. | Đúng. Câu "money in the required unit, such as integer cents" và "required metadata block" chỉ gợi ý, không đủ để tái tạo chính xác quy ước. | 11 dòng. `description` rõ ("structured data/log outputs ... schema, units, file layout"). Được đọc ở cả 3 tác vụ, nhưng `data-learn` và `logs-learn` vẫn trượt cả 3 check `rule_`: tác tử ghi `answer.json` với số thực USD và không có `meta`, vì skill không nói giá trị cụ thể của quy ước. |
| `code-change-hygiene` | Khá cụ thể cho họ `code`: không sửa test gốc, thêm test hồi quy, type annotation cho hàm public, changelog. Đây là đúng 3 quy ước `rule_` của `code-learn`, nhưng diễn đạt chung (không nêu tên tệp `test_regressions.py`, tiêu đề `## Unreleased` hay định dạng `fix(<fn>)`). | Đúng. Nhưng thiếu chi tiết định dạng nên khó đạt check, vì check đòi đúng tên tệp và đúng định dạng dòng. | 9 dòng. `description` nêu rõ khi sửa lỗi trong gói code. Được đọc ở cả 3 tác vụ (kể cả `data`, `logs`, không liên quan). Ở `code-learn` được làm theo từng dòng: đạt `rule_type_hints`; tạo `tests/test_regression.py` (quy ước cần `test_regressions.py`) và thêm changelog dưới `## Unreleased` nhưng không đúng định dạng `- fix(<function name>): ...`, nên trượt `rule_regression_tests` và `rule_changelog`. |

## 7. Kết quả so sánh (Phần 4.3, 4.4)


`report/table.md` (`python -m lab.compare`):

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 7/10 | 7/10 | 8/10 |
| data-learn | 5/8 | 5/8 | 5/8 |
| logs-learn | 0/9 | 6/9 | 6/9 |
| code-eval | 7/11 | 8/11 | 9/11 |
| data-eval | 0/9 | 5/9 | 5/9 |
| logs-eval | 6/10 | 6/10 | 6/10 |
| **Mean score - learning tasks** | 0.44 | 0.66 | 0.70 |
| **Mean score - evaluation tasks** | 0.41 | 0.63 | 0.66 |
| **Mean tokens per run** | 530,574 | 972,507 | 221,205 |
| **Runs that read a skill** | 0/6 | 0/6 | 6/6 |

`python scripts/check_breakdown.py`:

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval     13/18         0/12         467,577      0/3
baseline      learn    12/18         0/9          593,570      0/3
subagents     eval     18/18         1/12       1,120,560      0/3
subagents     learn    18/18         0/9          824,454      0/3
skills-auto   eval     18/18         2/12         211,740      3/3
skills-auto   learn    18/18         1/9          230,670      3/3
```

- Các lần chạy có `error`: tất cả là `GraphRecursionError` (hết 60 bước), không có lỗi hạ tầng trong bộ kết quả cuối. Gồm `baseline` code-learn, data-learn, logs-learn, data-eval, logs-eval (5/6); `subagents` data-eval (1/6); `skills-auto` code-eval, logs-learn (2/6). Theo GUIDE, các lần này được giữ nguyên và chấm trên trạng thái workspace lúc dừng. Các lần lỗi mạng đã được chạy lại (Phụ lục, mục 4).
- `skills_modified = true`: không có lần nào.
- `python scripts/verify_freeze.py`: "checked 6 runs of skill conditions: OK", chạy trong container Linux. Trên Windows, script báo sai "skills differ" vì `hash_skills` đưa đường dẫn tương đối có dấu `\` vào hash, trong khi các lần chạy diễn ra trên Linux (`/`). Đã kiểm chứng: `skills_sha256` của cả 6 lần chạy bằng `hash_skills` tính trên Linux (`571bd8ad...`).

## 8. Phân tích

1. **Điều kiện nào cải thiện điểm so với `baseline`?** Cả hai điều kiện đều cải thiện ở cả tác vụ học và tác vụ đánh giá, với mức tương đương nhau giữa hai vai trò. Tác vụ học: `subagents` +0,22 (0,44 → 0,66), `skills-auto` +0,26 (→ 0,70). Tác vụ đánh giá: `subagents` +0,22 (0,41 → 0,63), `skills-auto` +0,25 (→ 0,66). Không có điều kiện nào cải thiện tác vụ học mà không cải thiện tác vụ đánh giá, nên không thấy dấu hiệu quá khớp ở mức điểm tổng. Tuy nhiên, gần như toàn bộ phần cải thiện đến từ việc tránh hết bước, không đến từ tri thức. Ở `baseline`, 5/6 lần chạy hết 60 bước, và 2 tác vụ (`logs-learn`, `data-eval`) không ghi được tệp đầu ra nên 0 điểm. Hai điều kiện kia chỉ có 1-2 lần hết bước và đều kịp ghi đầu ra. Chênh lệch giữa `skills-auto` và `subagents` chỉ là 1 check ở `code-learn` và 1 check ở `code-eval`, nhỏ hơn biên nhiễu (câu 6, mục 9), nên không kết luận được điều kiện nào tốt hơn về điểm.
   - Đối chiếu giả thuyết: H1 **bị bác bỏ một phần**: `subagents` không xấp xỉ `baseline` mà cao hơn 0,22 trên tác vụ đánh giá, vì subagent nới ngân sách bước như đã dự đoán, nhưng hiệu ứng lớn hơn dự kiến; phần token thì đúng (gấp 1,8 lần). H2 **được ủng hộ**: `skills-auto` cao nhất (0,66) và rẻ nhất, dù hơn `subagents` chỉ 1 check. H3 **không được ủng hộ** ở điểm tổng (+0,26 so với +0,25), nhưng **được ủng hộ** ở check quy ước (câu 2).
2. **Tách check kỹ thuật và check quy ước.** Kỹ thuật: `baseline` 12/18 (học), 13/18 (đánh giá); `subagents` và `skills-auto` đạt 18/18 ở cả hai vai trò. Quy ước: `baseline` 0/9 và 0/12; `subagents` 0/9 và 1/12 (`rule_type_hints` ở `code-eval`); `skills-auto` 1/9 và 2/12 (`rule_type_hints` ở cả hai, cộng `rule_regression_tests` ở `code-eval`). Skill giúp chủ yếu nhóm check kỹ thuật, một cách gián tiếp: `work-from-given-spec` ngăn tác tử đốt hết bước khi lục tìm quy ước, nên nó kịp làm và ghi đầu ra. Với check quy ước, skill chỉ giúp ở họ `code`, nơi `code-change-hygiene` nêu đủ cụ thể (type annotation, test hồi quy). Ở họ `data` và `logs`, skill nêu quy ước quá chung chung ("money in the required unit, such as integer cents", "include the required metadata block exactly") nên 0/6 check `rule_` học và 0/8 check `rule_` đánh giá đạt. **Quy ước mới** của tác vụ đánh giá (`rule_version_bump`, `rule_sorted_keys_format`, `rule_source_line`) đạt 0/3 ở mọi điều kiện, vì không có trong phản hồi của tác vụ học nên curator không thể biết. Đây là giới hạn cơ bản của skill rút ra từ phản hồi.
3. **Một check skill giúp, một check skill không giúp.** `skills_read = 4` ở cả 6 lần chạy: tác tử đọc mọi `SKILL.md` ngay ở các tool call đầu tiên, đúng `SKILLS_NOTE`.
   - Giúp: `rule_type_hints` (`code-learn`, `code-eval`). `baseline` trượt check này ở cả hai tác vụ. Với `skills-auto`, câu trả lời cuối của `code-learn` liệt kê "Added type annotations" cho từng hàm sửa, và "House-rule checklist: ... public functions annotated ✔", lặp lại đúng dòng "Add type annotations to every public function parameter and return value" của `code-change-hygiene`.
   - Không giúp: `rule_changelog` (`code-learn`, `code-eval`). Skill được đọc và được làm theo: tác tử thêm bullet dưới `## Unreleased` ("Added a bullet under `## Unreleased` for each of the four fixes"). Nhưng skill chỉ nói "in the required format", không nêu định dạng `- fix(<function name>): ...`, nên check vẫn trượt. Đây là trường hợp skill thiếu chi tiết, không phải bị bỏ qua. Tương tự, `rule_regression_tests` trượt ở `code-learn` vì tác tử đặt tên `test_regression.py`, nhưng đạt ở `code-eval` với tên `test_regressions.py`: cùng một skill nhưng kết quả phụ thuộc vào lựa chọn tên ngẫu nhiên của mô hình.
4. **Chi phí.** Token trung bình mỗi lần (6 tác vụ): `baseline` 530.574, `subagents` 972.507 (gấp 1,8 lần), `skills-auto` 221.205 (bằng 0,42 lần). Điểm trên 100k token (điểm đánh giá trung bình chia token trung bình): `baseline` 0,41/5,31 = 0,077; `subagents` 0,63/9,73 = 0,065; `skills-auto` 0,66/2,21 = **0,30**, hiệu quả gấp khoảng 4 lần `baseline`. Đa tác tử **không đáng chi phí** ở đây: nó đạt điểm gần bằng `skills-auto` nhưng tốn gấp 4,4 lần token, cao nhất ở `logs-eval` với 1,74M token cho 6/10 điểm, cùng điểm với `skills-auto` dùng 105k token. Lợi ích của subagent chủ yếu là nới ngân sách bước của luồng chính, điều có thể đạt rẻ hơn bằng một skill dặn không tìm kiếm lan man. Cache tiền tố của DeepSeek: ở 6 lần chạy `skills-auto` sau freeze (lần đầu ghi trường `tokens.cache_read`), 1.152.896/1.231.151 token đầu vào (93,6%) được phục vụ từ cache. Phần lớn token đầu vào là lịch sử hội thoại gửi lại mỗi lượt, nên chi phí thực tế thấp hơn nhiều so với con số token thô.
5. **Rò rỉ dữ liệu và quá khớp.**
   - Rò rỉ trong skill: không có. `validate_skill` đã chặn một skill có chữ "orders" (trùng tên tệp đánh giá); 4 skill còn lại không nêu tên tác vụ, tên tệp riêng hay con số. Prompt của curator chỉ đọc `run.json` có `role == "learn"` (có test kiểm tra).
   - Rò rỉ qua môi trường: đây là rủi ro lớn nhất. Ở lần thử đầu tiên không cô lập, tác tử đọc được `tasks/data-eval/*` và `check.py`. Kết quả đó bị hủy và được thay bằng cơ chế chạy shell bằng `nobody` (Phụ lục, mục 2).
   - Quá khớp: thấp. Các skill chung chung đến mức không mang được giá trị quy ước cụ thể, nên lợi ích chuyển giao gần như nguyên vẹn (+0,26 học so với +0,25 đánh giá). Cái giá là chúng không giúp được các check quy ước ngoài họ `code`. Đây là hai mặt của cùng một lựa chọn trong prompt curator ("Skills must be general: do not mention ... answers or numbers").
6. **Nhiễu.** Cùng bộ skill trên tác vụ học, ở Phần 3.4 (`results/skills-auto-dev/`) và sau freeze: `code-learn` 8/10 → 8/10, `data-learn` 5/8 → 5/8, `logs-learn` 6/9 → 6/9. Chênh lệch điểm bằng 0 và các check trượt trùng nhau hoàn toàn, nhưng token dao động mạnh (171k → 143k, 116k → 179k, 170k → 370k), và `logs-learn` sau freeze có hết bước còn bản Phần 3.4 thì không. Ngược lại, `baseline` có nhiễu điểm rất lớn: `data-learn` 0/8 rồi 5/8, `logs-learn` 6/9 rồi 0/9. Như vậy độ nhiễu phụ thuộc điều kiện: khi tác tử có quy trình ổn định (`skills-auto`), điểm lặp lại tốt; khi tác tử lan man (`baseline`), việc kịp ghi đầu ra trước 60 bước gần như ngẫu nhiên. Khoảng cách `baseline` với hai điều kiện kia (khoảng 0,22-0,25) phù hợp với cơ chế quan sát được trong vết, nhưng độ lớn chính xác của nó không đáng tin (một lần chạy `baseline` khác có thể cho 0,6). Còn chênh 0,03 giữa `skills-auto` và `subagents` thì nằm trong nhiễu.

## 9. Hạn chế và tính hợp lệ


1. **Mỗi cấu hình chạy một lần, mà nhiễu rất lớn.** Cùng `baseline data-learn` cho 0/8 (lần 1) và 5/8 (lần 2); `baseline logs-learn` cho 6/9 (lần 1, bị ngắt do lỗi mạng) và 0/9 (lần 2). Chênh lệch lên tới 8-9 check giữa hai lần chạy giống hệt nhau, nên mọi khác biệt dưới khoảng 3 check mỗi tác vụ trong bảng mục 7 không đủ cơ sở để kết luận. Kết luận chỉ đáng tin ở các khác biệt lớn và nhất quán trên cả 3 họ tác vụ.
2. **Ngân sách bước (`recursion_limit = 60`) chi phối kết quả.** Với `deepseek-reasoner`, phần lớn thất bại của `baseline` là hết bước khi đang tìm quy ước ẩn (nhóm G), không phải sai kỹ thuật. Vì vậy phần lớn lợi ích của `skills-auto` đo được ở đây là lợi ích "đừng tìm kiếm lan man", chủ yếu do một skill (`work-from-given-spec`) mang lại. Với giới hạn bước lớn hơn hoặc một mô hình ít tò mò hơn, khoảng cách giữa các điều kiện có thể nhỏ hơn nhiều.
3. **Chỉ một mô hình và một nhà cung cấp.** `deepseek-chat` thậm chí không hoàn thành được tác vụ nào (lặp vô hạn). Kết quả không tổng quát hóa sang mô hình khác; GUIDE dự kiến mô hình mạnh làm đúng phần lớn check kỹ thuật ngay ở `baseline`.
4. **Ít tác vụ, và quy ước do giảng viên thiết kế.** Mỗi vai trò chỉ có 3 tác vụ (27 check học, 3 họ), nên một tác vụ hết bước làm thay đổi tỷ lệ đáng kể. Quy ước Acme chỉ học được qua `detail` của bot chấm; skill tự sinh vì thế phụ thuộc vào việc lần `baseline` có ghi được đầu ra hay không. Ví dụ, curator không thấy quy ước của họ `logs` vì `baseline logs-learn` hết bước trước khi ghi tệp.
5. **Môi trường thực thi tự dựng.** Cô lập bằng user `nobody` là thay đổi so với hướng dẫn (chạy `LocalShellBackend` trực tiếp). Nó cần thiết để tránh rò rỉ (Phụ lục, mục 2), nhưng làm các lệnh tìm kiếm của tác tử gặp "Permission denied" thay vì kết quả rỗng, có thể làm hành vi khác với môi trường của các nhóm khác.

## 10. Kết luận

Với `deepseek-reasoner`, thất bại chủ yếu của tác tử mặc định là lỗi quy ước (nhóm E: 0/21 check `rule_`) và hết ngân sách bước khi đi tìm các quy ước không tồn tại (5/6 lần chạy). Skill do curator tự sinh nâng điểm đánh giá từ 0,41 lên 0,66 và giảm token khoảng 2,4 lần (đọc ở 6/6 lần chạy), nhưng phần lớn lợi ích đến từ một skill quy trình chặn việc tìm kiếm lan man, không đến từ tri thức quy ước. Đa tác tử đạt điểm tương đương (0,63) nhưng tốn gấp 4,4 lần token `skills-auto`, nên không đáng chi phí trong thí nghiệm này. Skill không giúp được quy ước mới của tác vụ đánh giá (0/3) và chỉ giúp quy ước cũ khi nêu đủ cụ thể (2/12); với một lần chạy mỗi cấu hình và nhiễu `baseline` tới 8 check, mọi chênh lệch nhỏ hơn khoảng 0,1 không có ý nghĩa. Đề xuất tiếp theo: cho curator giữ nguyên văn định dạng quy ước từ `detail` (tên tệp, khóa, định dạng dòng), vì chúng là quy ước của tổ chức chứ không phải đáp án, rồi đo lại với ít nhất 3 lần chạy mỗi cấu hình (GUIDE 6e).

## Phụ lục

- Lệnh đã chạy (theo thứ tự), mọi lần chạy tác vụ đều qua `sh docker-run.sh ...`:
  1. `pytest tests` (29 passed, cả trên Windows và trong container).
  2. Thử `deepseek-chat` trên `data-learn` (3 lần, đều 0/8, `GraphRecursionError`; không giữ kết quả). Đổi sang `deepseek-reasoner`.
  3. `python -m lab.runner --condition baseline --tasks learn`; `--condition subagents --tasks learn`.
  4. Chạy lại `baseline data-learn logs-learn` (lần 1 của `logs-learn` lỗi mạng; lần 1 của `data-learn` hết bước). Lần 1 sao lưu ở `results/baseline-run1/`.
  5. `python -m lab.curator` (2 lần, xem mục 6).
  6. Sửa CRLF (xem dưới); chạy lại `code-learn` cho `baseline` và `subagents` (`subagents` lỗi mạng 2 lần, đến lần 3 mới chạy được); `--condition skills-auto --tasks learn`, sao lưu thành `results/skills-auto-dev/`.
- Tái lập:
  ```bash
  pip install -e . && pytest                    # 29 passed
  docker build -t lab-deepagents .
  # .env: LAB_MODEL=deepseek:deepseek-reasoner, DEEPSEEK_API_KEY=..., LAB_TEMPERATURE=0
  sh docker-run.sh python -m lab.runner --condition baseline --tasks all
  sh docker-run.sh python -m lab.runner --condition subagents --tasks all
  python -m lab.curator                          # skill đã đóng băng ở tag `freeze`
  sh docker-run.sh python -m lab.runner --condition skills-auto --tasks all
  python -m lab.compare > report/table.md && python scripts/check_breakdown.py && python scripts/verify_freeze.py
  ```
  Trên Windows: đặt `git config core.autocrlf input` trước khi clone hoặc checkout, nếu không bộ chấm của `code-*` (so hash tệp test) và `verify_freeze.py` (so hash skill) sẽ báo sai.
- Thử thách mở rộng (nếu có): không thực hiện.
- Ghi chú khác (sự cố hạ tầng và cách xử lý):
  1. **Shell trên Windows.** `LocalShellBackend` dùng `cmd.exe` trên Windows. `make_backend` chạy lệnh qua `bash -c` của Git for Windows khi `sys.platform == "win32"`; các test chấm vẫn đạt.
  2. **Rò rỉ dữ liệu qua shell, phát hiện ở lần thử đầu.** `LocalShellBackend` không cô lập: chạy trực tiếp trên Windows, tác tử mở các tệp `.tmp` trong thư mục Temp của người dùng; chạy trong Docker với repo mount ở `/lab`, tác tử tìm ra repo, đọc `tasks/data-learn/check.py`, `tasks/data-eval/*` và viết script giải chung cho cả hai tác vụ (reward hacking và rò rỉ dữ liệu đánh giá). Kết quả này bị hủy. Biện pháp: khi biến `LAB_AGENT_USER` được đặt và runner chạy bằng root, `make_backend` chạy lệnh shell của tác tử bằng user đó qua `setpriv`. Repo được mount ở `/root/lab` (`/root` có quyền 700), sandbox được mở quyền ghi trước mỗi lệnh (bỏ qua symlink, trừ `skills/` chỉ đọc). Đã kiểm chứng: shell nhận "Permission denied" với `/root/lab`, không có biến chứa khóa API, `ln -s /root` không mở được `/root`. Ở các lần chạy chính thức, vết vẫn cho thấy tác tử thử thoát ra (`/workspace/tests/../../lab/src/lab/curator.py`, `grep -r "Acme" /`), nhưng chỉ chạm tới mã harness cài trong image, không có bộ chấm hay dữ liệu đánh giá.
  3. **Line ending.** Git trên máy đặt `core.autocrlf=true` nên 16 tệp trong `tasks/` bị đổi sang CRLF; check `tests_not_modified` (so hash) của `code-learn` luôn trượt (hash `efb5e7…` so với `79e05f…`). Sửa bằng `git config core.autocrlf input` và checkout lại `tasks/`; các lần `code-learn` bị ảnh hưởng được sao lưu ở `results/crlf-backup/` và chạy lại. Các lần `data-learn` và `logs-learn` trước khi sửa được giữ lại: dữ liệu `sales.csv` vốn đã là LF, còn `app.log` dạng CRLF không làm trượt check kỹ thuật nào (lần `baseline-run1` của `logs-learn` đạt 6/6 check kỹ thuật).
  4. **Lỗi mạng tới API** (`OpenAIConnectionError`, `OpenAITimeoutError`) ở 4 lần chạy; đều được chạy lại, bản lỗi sao lưu trong `results/baseline-run1/` và `results/crlf-backup/`.
