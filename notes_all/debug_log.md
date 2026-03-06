# Debug Log

## Template
```
## Bug #X: [简短描述]
**Time**: HH:MM
**Context**: 我在做[任务]
**Symptom**: [错误信息/异常行为]
**Hypothesis**: 我猜是因为...
**Actual Cause**: 实际是...
**Solution**: 
**Learned**: 
---
```

## Bugs Encountered

Bug #1：OpenAI 一次发送太多数据

Symptom：invalid_request_error 400错误
Cause：把2000+个 chunk 一次性发给 OpenAI embedding API，超出限制
Solution：embed_texts 加 batch_size=100，分批发送

Bug #2：Pinecone upsert 数据量太大

Symptom：decoded message length too large: found 17MB, limit is 4MB
Cause：一次性把2082条 records 发给 Pinecone
Solution：用 for i in range(0, len(all_records), 100) 分批 upsert

Bug #3：变量名拼写错误导致 NameError

Symptom：response 未定义
Cause：存的时候写成 reponse，取的时候写成 response，不一致
Solution：统一变量名

Bug #4：ingest.py 路径找不到

Symptom：No such file or directory
Cause：ingest.py 在 notes_all/ 文件夹里，不在根目录
Solution：把文件移到根目录

Bug #5：for 循环遍历空列表

Symptom：load_docs 返回空结果
Cause：for doc in docs 应该是 for path in paths，遍历了空列表
Solution：改成遍历 paths

Bug #6：OpenAI 余额不足

Symptom：429 insufficient_quota
Cause：OpenAI 账号没有充值
Solution：充值 $5
---
```

---
