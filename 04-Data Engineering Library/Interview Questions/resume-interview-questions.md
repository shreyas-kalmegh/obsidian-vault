# Resume-Based Interview Questions

These questions are based on the projects and experience listed in [resume.md](/mnt/c/Users/shrey/projects/obsidian-vault/04-Data Engineering Library/Interview Questions/resume.md). They are phrased the way an interviewer would typically ask in a data engineering or data platform interview.

## Eventbrite

### Self-Service Data Platform
- Can you walk me through the self-service data platform you helped build at Eventbrite?
- What were the biggest architectural challenges in supporting 70+ Airflow tenants on a shared platform?
- How did you think about multi-tenancy, isolation, and platform guardrails?
- If a new team wanted to onboard onto the platform, what did that process look like end to end?
- What parts of the platform were standardized versus left flexible for tenants?
- Tell me about a production incident on the platform that taught you something important.
- How did you measure whether the platform was actually successful for internal users?

### Marketing Integration Platform / Reverse ETL
- You mentioned building a self-serve marketing integration platform. What problem was the business facing before this existed?
- Why did you choose a Reverse ETL approach with Hightouch instead of custom pipelines?
- Walk me through the architecture from raw source data to activated marketing audiences.
- What role did dbt models play in making the platform reusable and self-serve?
- How did you ensure data quality before syncing data into systems like Google Ads or Braze?
- What were the biggest challenges in aligning technical implementation with marketing stakeholders?
- You mentioned a 40% reduction in time-to-market. How was that measured?
- If you were redesigning that platform today, what would you do differently?

### Ingestion, Governance, Observability, and GDPR
- You worked across ingestion, transformation, governance, and observability. Which of those areas did you own most deeply?
- Can you compare how you handled CDC, batch, and API ingestion patterns on the platform?
- What does good observability look like for a modern data platform in your opinion?
- How did you design metadata or lineage workflows so teams could trust the data?
- Tell me about a time when data quality checks caught a serious downstream issue.
- How did GDPR requirements influence the design of your data pipelines and storage patterns?
- What tradeoffs did you make between governance and developer velocity?

### Airflow Platform Performance
- You improved Airflow performance using Celery Kubernetes Executor and KEDA. What was broken or painful before those changes?
- Why was Celery Kubernetes Executor the right fit for your use case?
- How did you approach autoscaling, and what signals did KEDA scale on?
- You mentioned reducing queue latency by 75 to 85 percent. What specifically changed to drive that improvement?
- What risks did you have to manage while changing the Airflow execution model?
- How did you validate that the new setup was stable in production?
- Can you talk about a time Airflow became a bottleneck and how you debugged it?

### RDS Proxy / Metadata Database Stability
- What issues were you seeing with the Airflow metadata database before introducing RDS Proxy?
- Why did you prefer RDS Proxy over simply scaling the database instance?
- How did you confirm the bottleneck was connection management rather than compute or storage?
- Were there any unexpected side effects after introducing the proxy layer?

### S3 Cost Optimization
- Walk me through the S3 cost optimization project that saved 83% in storage costs.
- How did you identify the main drivers of the storage bill?
- What lifecycle policies did you introduce, and how did you validate they were safe?
- Were there any teams concerned about retention or restore needs? How did you handle that?
- What would you say made this project more than just a simple housekeeping task?

### ML Deployment Platform
- You mentioned building CDK-based ML deployment pipelines. What problem existed before that work?
- What did the deployment workflow look like across dev, test, and prod?
- How did you implement blue-green deployment for SageMaker endpoints?
- What kinds of rollback conditions or health checks did you automate?
- How did Airflow integrate with the ML platform?
- What value did the Feature Store add, and what adoption challenges did you face?
- You mentioned 50 to 75 percent faster iteration cycles. What was slowing teams down before?
- If an interviewer asked whether this was more platform engineering or ML engineering, how would you answer?

### Streaming Analytics Platform
- Tell me about the streaming analytics platform using Pinot, Kafka, and Flink.
- What problem required real-time analytics instead of batch reporting?
- Why did you choose Pinot for serving and Flink for processing?
- What were the hardest parts of meeting sub-second p99 query latency?
- How did you think about correctness versus latency in the streaming pipeline?
- What kinds of late-arriving data or backfill problems did you run into?
- How did you monitor end-to-end freshness and serving health?

### Data Freshness Dependency Mechanism
- Can you explain the DynamoDB-backed data freshness dependency mechanism you built?
- What problem were downstream teams facing before this existed?
- Why did you choose DynamoDB for metadata and activity logging?
- How did the Airflow sensor-based checks work in practice?
- How did you avoid false positives or unnecessary blocking in dependent workflows?
- What alternatives did you consider, and why did you reject them?

### Mentorship and Ownership
- Tell me about a junior engineer or intern you mentored. What did you do, and what was the outcome?
- How do you balance shipping work yourself versus investing time in other engineers?
- Can you share an example of giving difficult technical feedback in a constructive way?

## Advance Auto Parts

### Identity Resolution Pipeline
- You worked on identity resolution across multiple source systems. How did you model the matching problem?
- What types of signals or keys were most useful for linking records?
- How did you think about precision versus recall in identity resolution?
- What were the hardest data quality issues in that pipeline?
- How did you validate whether the identity stitching logic was actually working?
- If two source systems disagreed, how did you decide which record won?

### NLP Review Insights Pipeline
- Walk me through the pipeline that extracted thematic tags from customer reviews.
- What NLP approach did you use, and how did you choose it?
- How did you move from raw text to something trustworthy enough for downstream analytics?
- What were the biggest challenges around noisy or ambiguous review data?
- How did business users consume the output?
- If the model or tagging quality drifted over time, how would you detect that?

## Red Hat

### Containerization and Platform Modernization
- Tell me about the services you containerized at Red Hat and why that migration mattered.
- What were the operational pain points before moving to OpenShift and Kubernetes?
- How did you decide what belonged in REST APIs versus batch workflows?
- What did GitLab CI/CD automate, and where did releases still require manual judgment?
- What was the most difficult part of getting legacy data processing services production-ready in Kubernetes?

### Sales Incentive Anomaly Detection
- You mentioned saving over $1 million through anomaly detection on Salesforce data. Can you walk me through that project?
- What kinds of anomalies were you trying to detect?
- Was this more of a rules engine, a statistical model, or a hybrid approach?
- How did you evaluate whether the detected anomalies were truly actionable?
- How did you work with business stakeholders to translate ambiguous compensation rules into logic?
- What was one tricky edge case that could have caused incorrect payouts?

### Airflow / Spark Migration
- You migrated workflows from Luigi and Pentaho to Airflow and Spark. What drove that migration?
- How did you decide which pipelines were worth moving first?
- What performance gains came from Spark versus better workflow orchestration?
- What challenges did you face in preserving correctness during the migration?
- If you had to do a migration like that again, what would you plan differently?

## Cross-Project Behavioral and System Design Questions

- Looking across your experience, what is the most technically complex data platform problem you have solved?
- Tell me about a time you had to make a tradeoff between speed of delivery and platform quality.
- Which project on your resume best demonstrates end-to-end ownership, and why?
- What is a project on your resume that sounds impressive on paper but was actually messy underneath?
- How do you decide when to build a platform capability versus solving a one-off team problem?
- Tell me about a time you influenced teams without formal authority.
- What is one project on your resume where the metrics improved, but the hard part was actually organizational rather than technical?
- Which system you built would be hardest for someone else to maintain if you left, and how would you reduce that risk?

## Drill-Down Questions Interviewers May Use

- What was your exact contribution versus the team’s contribution?
- What specific decisions did you personally make?
- What were the alternatives you considered?
- What broke in production?
- How did you know the solution was working?
- What was the business impact, and how confident are you in that number?
- What would you change if you had another quarter to improve it?
- Where did the design fall short?
- What tradeoffs did you knowingly accept?
- If I asked one of your teammates about this project, what would they say you owned?

## Best Projects To Prepare Deeply

- Eventbrite self-service data platform
- Eventbrite Airflow scaling and stability improvements
- Eventbrite marketing activation / Reverse ETL platform
- Eventbrite ML deployment platform
- Eventbrite streaming analytics platform
- Red Hat sales incentive anomaly detection
- Advance Auto Parts identity resolution pipeline
