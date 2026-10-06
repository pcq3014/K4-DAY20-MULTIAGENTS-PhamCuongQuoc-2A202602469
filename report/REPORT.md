# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Phạm Cường Quốc | 2A202602469 | Toàn bộ |

- Mô hình (tên deployment hoặc `LAB_MODEL`), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `deepseek:deepseek-reasoner`, `LAB_TEMPERATURE=0`, `recursion_limit=60`. Ban đầu dùng `deepseek:deepseek-chat`, nhưng 3 lần thử trên `data-learn` (nhiệt độ 0 và 0,5) đều đạt 0/8 vì chạm `GraphRecursionError`: mô hình đi tìm tệp "Acme conventions" khắp hệ thống tệp rồi lặp lại đúng một lệnh `ls` hơn 15 lần (436k-905k token mỗi lần). Các lần thử này không tính vào kết quả.
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Python 3.12, chạy trong Docker (`python:3.12-slim`, nhân WSL2) trên Windows 10 qua `docker-run.sh`. Shell của tác tử chạy bằng user `nobody` (`LAB_AGENT_USER`), repo mount ở `/root/lab` (quyền 700), nên tác tử không đọc được bộ chấm, tác vụ đánh giá hay kết quả cũ (xem Phụ lục).
- Số lần chạy tác vụ đã dùng / ngân sách: đến trước `freeze` là 21 lần. Trong đó có 5 lần thử cấu hình (4 lần `deepseek-chat`, 1 lần thử `deepseek-reasoner`), 4 lần lỗi hạ tầng hoặc bị dừng (3 lần lỗi mạng, 1 lần chạy dở), 2 lần `code-learn` không hợp lệ do lỗi CRLF, và 10 lần dùng trong báo cáo (9 lần chính thức và lần 1 của `baseline data-learn`, dùng để đo nhiễu).
- Commit của tag `freeze`:

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

> Dự đoán điều kiện nào đạt điểm cao nhất trên **tác vụ đánh giá** và vì sao. Nêu căn cứ từ phân loại lỗi (mục 4) và từ tài liệu tham khảo. Điền cả ba dòng; `verify_freeze.py` kiểm tra điều này.

- H1 (subagents so với baseline): Trên tác vụ đánh giá, `subagents` đạt điểm xấp xỉ `baseline` (chênh không quá 1 check mỗi tác vụ) nhưng tốn token nhiều hơn hoặc bằng. Căn cứ: trên tác vụ học cả hai đạt 12/18 check kỹ thuật và 0/9 check quy ước; lời giao việc chép đủ quy tắc của đề nhưng không thể chứa quy ước Acme vì tác tử chính không biết chúng (lỗi nhóm E). Subagent chỉ giúp tránh hết `recursion_limit`, vì việc của subagent không tính vào số bước của luồng chính (`subagents` 0/3 lần lỗi so với `baseline` 3/3 ở lần chạy cuối), đổi lại tốn nhiều token (`logs-learn` 1,16M).
- H2 (skills-auto so với baseline): `skills-auto` đạt điểm cao nhất trên tác vụ đánh giá, chủ yếu nhờ check kỹ thuật (ít lần hết bước hơn nhờ `work-from-given-spec`), và tốn ít token nhất. Check quy ước chỉ cải thiện ở các quy ước cũ được skill nêu chung chung (type hints, cent, UTC); check quy ước MỚI của tác vụ đánh giá sẽ không đạt vì không skill nào chứa nó. Căn cứ: trên tác vụ học `skills-auto` 18/18 kỹ thuật và 1/9 quy ước với 152k token/lần, so với `baseline` 12/18, 0/9 và 594k. SkillsBench ghi nhận skill tự sinh trung bình không có lợi; ở đây lợi ích đến từ việc chặn một hành vi xấu cụ thể chứ không phải từ tri thức miền.
- H3 (tác vụ học so với tác vụ đánh giá): Mức cải thiện của `skills-auto` so với `baseline` trên tác vụ đánh giá nhỏ hơn trên tác vụ học, nhất là ở check quy ước, vì skill thiếu chi tiết định dạng và tác vụ đánh giá có quy ước mới (đúng với SkillEvolBench về việc lợi ích không chuyển giao). Tuy vậy, phần cải thiện về quy trình (không lục hệ thống tệp, kiểm chứng tệp đầu ra) sẽ chuyển giao được. Nhiễu lớn: cùng cấu hình `baseline data-learn` cho 0/8 và 5/8 ở hai lần chạy, nên mọi chênh lệch nhỏ hơn khoảng 3 check mỗi tác vụ cần coi là không chắc chắn.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có 9 công cụ: công cụ tệp `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`; công cụ shell `execute`; công cụ giao việc `task`. Chỉ `execute` cho phép chạy lệnh (shell thật của backend).
2. `task` "launch an ephemeral subagent"; subagent mặc định `general-purpose` dùng cho nghiên cứu, tìm kiếm và tác vụ nhiều bước, "has access to all tools as the main agent". Mỗi lần gọi là stateless: "the agent sees only the prompt you give it and returns a single final report", tức là subagent KHÔNG thấy lịch sử hội thoại, system prompt hay kết quả công cụ của tác tử chính, chỉ thấy lời giao việc.
3. Câu từ `task`: "Put full detail in the prompt and state exactly what it should return". Câu từ `execute`: "You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search." Đáng chú ý, mô tả `execute` còn dặn "Use absolute paths and avoid `cd`", mâu thuẫn với `PATHS_NOTE` ("never starts with '/'"). Đây là nguyên nhân mô hình liên tục thử `/workspace` trong shell (thấy trong vết `data-learn`).

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

> Chỉ dùng tác vụ học. Mỗi dòng là một check thất bại.

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
- Ảnh hưởng đến token và thời gian: token trung bình `subagents` 824k/lần so với `baseline` 594k (tăng khoảng 1,4 lần), cao nhất `logs-learn` 1,16M (2 subagent). Thời gian 239-280 giây so với 117-257 giây. Điểm bằng nhau (12/18 kỹ thuật, 0/9 quy ước), nhưng `subagents` không lần nào hết `recursion_limit`, trong khi `baseline` hết cả 3 lần ở lần chạy cuối. Phần việc giao cho subagent không tính vào 60 bước của luồng chính, nên đa tác tử ở đây hoạt động như một cách nới ngân sách bước, với cái giá là token.

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

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
(dán bảng ở đây)
```

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Nhóm đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1.
2.
3.

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự), mọi lần chạy tác vụ đều qua `sh docker-run.sh ...`:
  1. `pytest tests` (29 passed, cả trên Windows và trong container).
  2. Thử `deepseek-chat` trên `data-learn` (3 lần, đều 0/8, `GraphRecursionError`; không giữ kết quả). Đổi sang `deepseek-reasoner`.
  3. `python -m lab.runner --condition baseline --tasks learn`; `--condition subagents --tasks learn`.
  4. Chạy lại `baseline data-learn logs-learn` (lần 1 của `logs-learn` lỗi mạng; lần 1 của `data-learn` hết bước). Lần 1 sao lưu ở `results/baseline-run1/`.
  5. `python -m lab.curator` (2 lần, xem mục 6).
  6. Sửa CRLF (xem dưới); chạy lại `code-learn` cho `baseline` và `subagents` (`subagents` lỗi mạng 2 lần, đến lần 3 mới chạy được); `--condition skills-auto --tasks learn`, sao lưu thành `results/skills-auto-dev/`.
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác (sự cố hạ tầng và cách xử lý):
  1. **Shell trên Windows.** `LocalShellBackend` dùng `cmd.exe` trên Windows. `make_backend` chạy lệnh qua `bash -c` của Git for Windows khi `sys.platform == "win32"`; các test chấm vẫn đạt.
  2. **Rò rỉ dữ liệu qua shell, phát hiện ở lần thử đầu.** `LocalShellBackend` không cô lập: chạy trực tiếp trên Windows, tác tử mở các tệp `.tmp` trong thư mục Temp của người dùng; chạy trong Docker với repo mount ở `/lab`, tác tử tìm ra repo, đọc `tasks/data-learn/check.py`, `tasks/data-eval/*` và viết script giải chung cho cả hai tác vụ (reward hacking và rò rỉ dữ liệu đánh giá). Kết quả này bị hủy. Biện pháp: khi biến `LAB_AGENT_USER` được đặt và runner chạy bằng root, `make_backend` chạy lệnh shell của tác tử bằng user đó qua `setpriv`. Repo được mount ở `/root/lab` (`/root` có quyền 700), sandbox được mở quyền ghi trước mỗi lệnh (bỏ qua symlink, trừ `skills/` chỉ đọc). Đã kiểm chứng: shell nhận "Permission denied" với `/root/lab`, không có biến chứa khóa API, `ln -s /root` không mở được `/root`. Ở các lần chạy chính thức, vết vẫn cho thấy tác tử thử thoát ra (`/workspace/tests/../../lab/src/lab/curator.py`, `grep -r "Acme" /`), nhưng chỉ chạm tới mã harness cài trong image, không có bộ chấm hay dữ liệu đánh giá.
  3. **Line ending.** Git trên máy đặt `core.autocrlf=true` nên 16 tệp trong `tasks/` bị đổi sang CRLF; check `tests_not_modified` (so hash) của `code-learn` luôn trượt (hash `efb5e7…` so với `79e05f…`). Sửa bằng `git config core.autocrlf input` và checkout lại `tasks/`; các lần `code-learn` bị ảnh hưởng được sao lưu ở `results/crlf-backup/` và chạy lại. Các lần `data-learn` và `logs-learn` trước khi sửa được giữ lại: dữ liệu `sales.csv` vốn đã là LF, còn `app.log` dạng CRLF không làm trượt check kỹ thuật nào (lần `baseline-run1` của `logs-learn` đạt 6/6 check kỹ thuật).
  4. **Lỗi mạng tới API** (`OpenAIConnectionError`, `OpenAITimeoutError`) ở 4 lần chạy; đều được chạy lại, bản lỗi sao lưu trong `results/baseline-run1/` và `results/crlf-backup/`.
