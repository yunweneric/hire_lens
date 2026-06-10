"""Curated job postings for database seeding."""

from __future__ import annotations

from typing import TypedDict


class JobSpec(TypedDict):
    title: str
    skills: list[str]
    department: str
    location: str
    employment_type: str
    summary: str
    about: str
    responsibilities: list[str]
    requirements: list[str]
    nice_to_have: list[str]


def build_description(spec: JobSpec) -> str:
    """Render a consistent, readable Markdown job description."""
    responsibilities = "\n".join(f"- {item}" for item in spec["responsibilities"])
    requirements = "\n".join(f"- {item}" for item in spec["requirements"])
    nice_to_have = "\n".join(f"- {item}" for item in spec["nice_to_have"])
    skills = ", ".join(spec["skills"])

    return f"""# {spec["title"]}

{spec["summary"]}

| | |
|---|---|
| **Department** | {spec["department"]} |
| **Location** | {spec["location"]} |
| **Employment** | {spec["employment_type"]} |
| **Key skills** | {skills} |

## About the role

{spec["about"]}

## What you will do

{responsibilities}

## What we are looking for

{requirements}

## Nice to have

{nice_to_have}

## How we work

We keep planning lightweight, ship in small iterations, and review work with kindness and clarity. You will partner closely with product and design, participate in architecture discussions, and help us raise the bar for quality without slowing delivery.

## Benefits

- Competitive compensation and meaningful equity
- Flexible remote-friendly schedule with core collaboration hours
- Annual learning budget for courses, books, and conferences
- Home office stipend and ergonomic equipment support
- Inclusive team culture with paid volunteer days

---

*HireLens is an equal opportunity employer. We welcome applicants from all backgrounds and do not discriminate on the basis of race, gender, identity, orientation, disability, or veteran status.*
"""


JOB_CATALOG: list[JobSpec] = [
    {
        "title": "Senior Backend Engineer",
        "skills": ["Python", "Django", "PostgreSQL", "REST APIs", "Docker"],
        "department": "Engineering",
        "location": "Remote (US & Canada)",
        "employment_type": "Full-time",
        "summary": (
            "Build reliable APIs and data services that power hiring workflows "
            "for thousands of candidates and recruiters."
        ),
        "about": (
            "You will own backend services from design through production, "
            "working on authentication, job pipelines, resume ingestion, and "
            "integrations with third-party ATS platforms. Our stack is "
            "Python-first with Django, PostgreSQL, and containerized deployments."
        ),
        "responsibilities": [
            "Design and implement scalable REST APIs with clear contracts and versioning.",
            "Model relational data carefully and tune queries for high-traffic read paths.",
            "Write automated tests across unit, integration, and API layers.",
            "Collaborate with frontend and ML teams on feature delivery and observability.",
            "Participate in on-call rotation and lead blameless incident reviews.",
        ],
        "requirements": [
            "5+ years building production backend systems in Python.",
            "Strong experience with Django or a comparable web framework.",
            "Comfortable designing schemas and migrations in PostgreSQL.",
            "Practical knowledge of containerization and CI/CD pipelines.",
            "Clear written communication for RFCs, runbooks, and code reviews.",
        ],
        "nice_to_have": [
            "Experience with Celery, Redis, or event-driven architectures.",
            "Background in HR tech, recruiting, or document processing pipelines.",
            "Familiarity with OpenAPI and API gateway patterns.",
        ],
    },
    {
        "title": "Frontend Developer",
        "skills": ["TypeScript", "React", "Tailwind CSS", "Accessibility", "Testing"],
        "department": "Engineering",
        "location": "Remote (Global)",
        "employment_type": "Full-time",
        "summary": (
            "Craft polished, accessible interfaces for recruiters and candidates "
            "across our public job board and internal admin tools."
        ),
        "about": (
            "Our frontend emphasizes clarity, performance, and inclusive design. "
            "You will ship responsive pages, reusable components, and thoughtful "
            "interaction patterns that make complex hiring data easy to understand."
        ),
        "responsibilities": [
            "Build and maintain React features with TypeScript and modern hooks patterns.",
            "Translate Figma designs into accessible, responsive UI with Tailwind CSS.",
            "Improve frontend performance through code splitting and asset optimization.",
            "Add tests with React Testing Library and contribute to design system guidelines.",
            "Partner with backend engineers on API shapes that improve user experience.",
        ],
        "requirements": [
            "4+ years of professional frontend development experience.",
            "Strong proficiency in React, TypeScript, and component-driven architecture.",
            "Working knowledge of WCAG accessibility standards and semantic HTML.",
            "Experience integrating REST APIs and handling loading, empty, and error states.",
            "Comfortable using Git, code review, and iterative delivery practices.",
        ],
        "nice_to_have": [
            "Experience with Next.js or server-rendered Django templates.",
            "Familiarity with Storybook or component documentation workflows.",
            "Eye for typography, spacing, and micro-interactions.",
        ],
    },
    {
        "title": "DevOps Engineer",
        "skills": ["AWS", "Kubernetes", "Terraform", "CI/CD", "Linux"],
        "department": "Platform",
        "location": "Remote (US & EU)",
        "employment_type": "Full-time",
        "summary": (
            "Automate infrastructure, harden deployments, and keep our hiring "
            "platform fast, secure, and easy to operate."
        ),
        "about": (
            "You will improve how we build, test, and release software. That "
            "includes infrastructure as code, observability, secrets management, "
            "and cost-aware scaling across staging and production environments."
        ),
        "responsibilities": [
            "Maintain Terraform modules and Kubernetes workloads for core services.",
            "Build CI/CD pipelines that support safe, frequent releases.",
            "Implement monitoring, alerting, and SLO dashboards for critical paths.",
            "Harden network policies, IAM roles, and backup/disaster recovery procedures.",
            "Support engineering teams with self-service deployment tooling.",
        ],
        "requirements": [
            "4+ years in DevOps, platform, or infrastructure engineering roles.",
            "Hands-on experience with AWS and container orchestration.",
            "Proficiency writing Infrastructure as Code with Terraform or similar tools.",
            "Strong Linux administration and troubleshooting skills.",
            "Security-minded approach to secrets, patching, and least-privilege access.",
        ],
        "nice_to_have": [
            "Experience with GitHub Actions, GitLab CI, or Argo CD.",
            "Background supporting Python/Django applications in production.",
            "Familiarity with SOC 2 or ISO 27001 control environments.",
        ],
    },
    {
        "title": "Data Scientist",
        "skills": ["Python", "SQL", "Statistics", "scikit-learn", "Experimentation"],
        "department": "Data",
        "location": "Hybrid — Austin, TX",
        "employment_type": "Full-time",
        "summary": (
            "Turn hiring funnel data into insights that help teams make better "
            "decisions about sourcing, screening, and candidate experience."
        ),
        "about": (
            "You will analyze product usage, design experiments, and build models "
            "that quantify resume quality, skill fit, and recruiter efficiency. "
            "Your work informs both product strategy and ML feature development."
        ),
        "responsibilities": [
            "Define metrics and dashboards for funnel conversion and model performance.",
            "Run A/B tests and quasi-experiments with sound statistical methodology.",
            "Prototype predictive models for ranking, segmentation, and anomaly detection.",
            "Partner with engineering to productionize high-value analyses.",
            "Present findings clearly to product, leadership, and non-technical stakeholders.",
        ],
        "requirements": [
            "3+ years in data science or analytics roles with product impact.",
            "Strong Python skills and fluency in SQL for exploratory analysis.",
            "Solid foundation in probability, inference, and experimental design.",
            "Experience with scikit-learn or comparable ML libraries.",
            "Ability to communicate uncertainty and trade-offs in plain language.",
        ],
        "nice_to_have": [
            "Experience in HR tech, marketplaces, or two-sided platforms.",
            "Familiarity with dbt, Airflow, or modern analytics stacks.",
            "Exposure to causal inference or uplift modeling techniques.",
        ],
    },
    {
        "title": "Machine Learning Engineer",
        "skills": ["Python", "PyTorch", "NLP", "MLOps", "Feature Engineering"],
        "department": "AI",
        "location": "Remote (US)",
        "employment_type": "Full-time",
        "summary": (
            "Ship production ML systems that parse resumes, extract skills, and "
            "score candidate–role fit with transparency and reliability."
        ),
        "about": (
            "Our ML team focuses on practical NLP for unstructured hiring documents. "
            "You will own model training pipelines, evaluation harnesses, and the "
            "serving layer that powers real-time analysis in the product."
        ),
        "responsibilities": [
            "Build and maintain training pipelines for resume parsing and skill extraction.",
            "Design offline and online evaluation metrics aligned with user outcomes.",
            "Deploy models with versioning, monitoring, and rollback strategies.",
            "Optimize inference latency and cost for high-volume document processing.",
            "Collaborate with data scientists on labeling guidelines and dataset quality.",
        ],
        "requirements": [
            "4+ years building ML systems in production environments.",
            "Strong Python engineering skills beyond notebook prototyping.",
            "Experience with NLP tasks such as classification, NER, or embeddings.",
            "Understanding of MLOps practices: feature stores, model registries, CI for ML.",
            "Comfort debugging data drift, bias, and failure modes in live systems.",
        ],
        "nice_to_have": [
            "Experience with LLM prompting, RAG, or fine-tuning workflows.",
            "Background in information retrieval or learning-to-rank systems.",
            "Familiarity with GPU scheduling and batch inference optimization.",
        ],
    },
    {
        "title": "Full Stack Developer",
        "skills": ["Python", "React", "PostgreSQL", "REST APIs", "GraphQL"],
        "department": "Engineering",
        "location": "Remote (Americas)",
        "employment_type": "Full-time",
        "summary": (
            "Own features end to end — from database schema and API design through "
            "to polished UI — across our hiring platform."
        ),
        "about": (
            "Full stack engineers at HireLens move fluidly between backend and "
            "frontend work. You will deliver complete user journeys such as job "
            "posting, application review, and recruiter dashboards."
        ),
        "responsibilities": [
            "Implement full features spanning Django models, APIs, and React views.",
            "Design pragmatic database schemas and migration strategies.",
            "Ensure consistent validation and error handling across client and server.",
            "Write tests that cover critical business logic and user flows.",
            "Review pull requests and help maintain shared coding standards.",
        ],
        "requirements": [
            "3+ years shipping full stack web applications in production.",
            "Proficiency in Python web frameworks and modern React development.",
            "Experience with relational databases and API design best practices.",
            "Ability to break large initiatives into incremental, releasable milestones.",
            "Strong product sense and empathy for both recruiters and candidates.",
        ],
        "nice_to_have": [
            "Experience with GraphQL or typed API clients.",
            "Familiarity with Tailwind CSS and design system workflows.",
            "Prior work on document upload, parsing, or workflow tools.",
        ],
    },
    {
        "title": "Product Designer",
        "skills": ["Figma", "UX Research", "Prototyping", "Design Systems", "UI"],
        "department": "Design",
        "location": "Remote (US & UK)",
        "employment_type": "Full-time",
        "summary": (
            "Shape intuitive hiring experiences that help teams evaluate talent "
            "fairly while keeping candidates informed and respected."
        ),
        "about": (
            "You will lead design from discovery through delivery, partnering with "
            "product and engineering on flows for job creation, application review, "
            "and AI-assisted insights. We value systems thinking and crisp craft."
        ),
        "responsibilities": [
            "Run discovery sessions, journey maps, and usability tests with target users.",
            "Produce wireframes, high-fidelity mocks, and interactive prototypes in Figma.",
            "Contribute to and extend our design system with reusable components.",
            "Define interaction patterns for complex data tables, filters, and dashboards.",
            "Present design rationale and iterate quickly based on feedback and metrics.",
        ],
        "requirements": [
            "4+ years designing B2B SaaS or workflow-heavy products.",
            "Strong portfolio demonstrating end-to-end UX and visual design craft.",
            "Experience facilitating research and synthesizing insights into decisions.",
            "Ability to design accessible interfaces that work across breakpoints.",
            "Collaborative working style with product managers and engineers.",
        ],
        "nice_to_have": [
            "Experience designing admin tools or HR/recruiting products.",
            "Familiarity with markdown editors or content authoring experiences.",
            "Motion design skills for subtle, purposeful UI feedback.",
        ],
    },
    {
        "title": "QA Automation Engineer",
        "skills": ["Python", "Pytest", "Playwright", "CI/CD", "Test Strategy"],
        "department": "Engineering",
        "location": "Remote (Global)",
        "employment_type": "Full-time",
        "summary": (
            "Raise release confidence with thoughtful test automation across APIs, "
            "UI flows, and critical hiring workflows."
        ),
        "about": (
            "Quality is a team responsibility, and you will be its champion. You will "
            "build reliable automation, define test plans for new features, and help "
            "engineers catch regressions before they reach production."
        ),
        "responsibilities": [
            "Develop automated API and browser tests for high-risk user journeys.",
            "Maintain test suites in CI with clear reporting and flake management.",
            "Partner with engineers to improve testability of new features.",
            "Define regression strategies for releases and hotfix validation.",
            "Document quality standards and mentor teammates on testing practices.",
        ],
        "requirements": [
            "3+ years in QA engineering with meaningful automation ownership.",
            "Strong Python skills and experience with pytest or similar frameworks.",
            "Hands-on experience with Playwright, Cypress, or Selenium.",
            "Understanding of CI/CD integration and environment management.",
            "Analytical mindset for reproducing bugs and identifying root causes.",
        ],
        "nice_to_have": [
            "Experience testing Django applications or React SPAs.",
            "Background in performance or load testing.",
            "Familiarity with contract testing for service integrations.",
        ],
    },
    {
        "title": "Mobile Engineer (iOS)",
        "skills": ["Swift", "SwiftUI", "UIKit", "REST APIs", "Core Data"],
        "department": "Engineering",
        "location": "Remote (US)",
        "employment_type": "Full-time",
        "summary": (
            "Build a native iOS experience that lets recruiters review applications "
            "and collaborate on the go."
        ),
        "about": (
            "Our mobile roadmap starts with recruiter workflows: notifications, "
            "application triage, and lightweight candidate review. You will set "
            "engineering standards for the iOS codebase as an early mobile hire."
        ),
        "responsibilities": [
            "Implement SwiftUI screens with clean architecture and testable view models.",
            "Integrate secure authentication and offline-friendly data caching.",
            "Collaborate with design on iOS-native patterns and accessibility.",
            "Instrument analytics and crash reporting for production monitoring.",
            "Publish releases through TestFlight and the App Store review process.",
        ],
        "requirements": [
            "4+ years shipping iOS applications to production.",
            "Proficiency in Swift, SwiftUI, and Apple's Human Interface Guidelines.",
            "Experience consuming REST APIs and handling auth token lifecycles.",
            "Solid understanding of memory management, concurrency, and app lifecycle.",
            "Comfort with XCTest and UI testing fundamentals.",
        ],
        "nice_to_have": [
            "Experience with Core Data, CloudKit, or local encryption patterns.",
            "Background building B2B or productivity mobile apps.",
            "Familiarity with Fastlane or automated release tooling.",
        ],
    },
    {
        "title": "Cloud Solutions Architect",
        "skills": ["AWS", "Networking", "Security", "Microservices", "Cost Optimization"],
        "department": "Platform",
        "location": "Remote (US & EU)",
        "employment_type": "Full-time",
        "summary": (
            "Design secure, scalable cloud architectures that support rapid product "
            "growth without sacrificing reliability or cost discipline."
        ),
        "about": (
            "You will guide major infrastructure decisions, review system designs, "
            "and partner with engineering leads on multi-region strategy, disaster "
            "recovery, and compliance-ready platform patterns."
        ),
        "responsibilities": [
            "Create architecture diagrams, ADRs, and migration plans for platform initiatives.",
            "Evaluate build-vs-buy decisions for messaging, search, and storage systems.",
            "Lead security reviews for network topology, IAM, and data protection controls.",
            "Coach teams on cloud-native patterns, observability, and operational readiness.",
            "Track cloud spend and recommend optimizations without compromising SLAs.",
        ],
        "requirements": [
            "7+ years in software or infrastructure engineering with architecture ownership.",
            "Deep AWS knowledge across compute, networking, storage, and identity.",
            "Experience designing microservice platforms with clear service boundaries.",
            "Strong grasp of encryption, secrets management, and compliance fundamentals.",
            "Excellent communication skills for technical and executive audiences.",
        ],
        "nice_to_have": [
            "AWS Solutions Architect Professional or Security Specialty certification.",
            "Experience in regulated industries or customer-driven audit programs.",
            "Background with multi-tenant SaaS architecture.",
        ],
    },
    {
        "title": "Engineering Manager",
        "skills": ["People Leadership", "Hiring", "Agile Delivery", "Technical Mentorship", "Roadmapping"],
        "department": "Engineering",
        "location": "Hybrid — New York, NY",
        "employment_type": "Full-time",
        "summary": (
            "Lead a high-performing engineering team building the core hiring "
            "platform while growing careers and maintaining technical excellence."
        ),
        "about": (
            "You will manage a team of 6–8 engineers working on job workflows and "
            "application review. This is a hands-on leadership role: you will unblock "
            "delivery, run effective rituals, and stay close enough to code to guide decisions."
        ),
        "responsibilities": [
            "Coach engineers through 1:1s, feedback, and individualized growth plans.",
            "Partner with product on roadmap prioritization and realistic commitments.",
            "Drive hiring loops, onboarding, and inclusive team culture.",
            "Remove organizational blockers and improve engineering processes.",
            "Contribute to architecture discussions and uphold quality standards.",
        ],
        "requirements": [
            "3+ years engineering management experience in product software teams.",
            "Prior background as a strong individual contributor in backend or full stack roles.",
            "Track record of shipping customer-facing features on predictable cadences.",
            "Experience recruiting and retaining diverse engineering talent.",
            "Clear, empathetic communication during change and incident response.",
        ],
        "nice_to_have": [
            "Experience managing distributed or remote-first teams.",
            "Familiarity with HR tech products or workflow automation domains.",
            "Exposure to budget planning and headcount forecasting.",
        ],
    },
    {
        "title": "Site Reliability Engineer",
        "skills": ["SRE", "Observability", "Python", "Kubernetes", "Incident Response"],
        "department": "Platform",
        "location": "Remote (US)",
        "employment_type": "Full-time",
        "summary": (
            "Improve reliability for services that recruiters depend on during "
            "critical hiring cycles."
        ),
        "about": (
            "As an SRE, you balance feature velocity with operational excellence. "
            "You will define SLOs, reduce toil through automation, and help the "
            "organization learn from incidents without blame."
        ),
        "responsibilities": [
            "Establish SLIs, SLOs, and error budgets for customer-facing services.",
            "Build tooling for deployment safety, rollbacks, and chaos experiments.",
            "Lead incident response, postmortems, and follow-up action tracking.",
            "Automate repetitive operational tasks and improve runbook quality.",
            "Partner with development teams on capacity planning and performance tuning.",
        ],
        "requirements": [
            "4+ years in SRE, platform, or production engineering roles.",
            "Strong scripting skills in Python or Go for automation.",
            "Experience with metrics, logging, and tracing stacks such as Prometheus or Grafana.",
            "Comfort running on-call and coordinating cross-team incident response.",
            "Pragmatic approach to reliability investments based on business risk.",
        ],
        "nice_to_have": [
            "Experience with Kubernetes operators or service mesh tooling.",
            "Background in ML serving infrastructure or document processing workloads.",
            "Familiarity with status page communication and customer impact assessment.",
        ],
    },
    {
        "title": "Security Engineer",
        "skills": ["Application Security", "Threat Modeling", "Python", "AWS Security", "Compliance"],
        "department": "Security",
        "location": "Remote (US & Canada)",
        "employment_type": "Full-time",
        "summary": (
            "Protect candidate and employer data by embedding security into how we "
            "design, build, and operate the HireLens platform."
        ),
        "about": (
            "You will partner with engineering from the earliest design stages, run "
            "threat models, improve secure SDLC practices, and respond to vulnerabilities "
            "with urgency and transparency."
        ),
        "responsibilities": [
            "Perform threat modeling and security design reviews for new features.",
            "Maintain SAST/DAST pipelines and triage findings with engineering teams.",
            "Lead vulnerability management, patching priorities, and penetration test remediation.",
            "Develop security training, standards, and guardrails developers can adopt easily.",
            "Support compliance efforts related to access control, logging, and data retention.",
        ],
        "requirements": [
            "4+ years in application or product security roles.",
            "Hands-on experience securing cloud-native web applications.",
            "Understanding of OWASP Top 10, SSRF, injection, and auth/session risks.",
            "Ability to communicate risk in terms of likelihood, impact, and mitigation options.",
            "Familiarity with AWS security services and IAM policy design.",
        ],
        "nice_to_have": [
            "Experience in SOC 2, ISO 27001, or GDPR-driven security programs.",
            "Background with bug bounty triage or red team collaboration.",
            "Knowledge of secrets rotation, KMS usage, and encryption at rest/in transit.",
        ],
    },
    {
        "title": "Technical Product Manager",
        "skills": ["Product Strategy", "Roadmapping", "User Research", "Agile", "Data Analysis"],
        "department": "Product",
        "location": "Remote (US)",
        "employment_type": "Full-time",
        "summary": (
            "Define and deliver product capabilities that help hiring teams move "
            "faster while improving fairness and transparency."
        ),
        "about": (
            "You will own a portfolio of features across job management, application "
            "review, and AI-assisted insights. We are looking for a TPM who can translate "
            "customer pain into clear specs engineers love to build."
        ),
        "responsibilities": [
            "Discover customer problems through interviews, support tickets, and usage data.",
            "Write PRDs, acceptance criteria, and phased rollout plans.",
            "Prioritize roadmap items based on impact, effort, and strategic fit.",
            "Coordinate launches with design, engineering, marketing, and customer success.",
            "Define success metrics and iterate based on quantitative and qualitative feedback.",
        ],
        "requirements": [
            "4+ years product management experience in B2B SaaS.",
            "Technical fluency sufficient to discuss APIs, data models, and ML limitations.",
            "Strong written communication for specs, release notes, and stakeholder updates.",
            "Experience working with design and engineering in agile delivery models.",
            "Comfort making trade-offs under ambiguity with sound judgment.",
        ],
        "nice_to_have": [
            "Background in HR tech, recruiting tools, or workflow software.",
            "Experience launching AI-powered features with responsible UX patterns.",
            "Familiarity with SQL or product analytics tools.",
        ],
    },
    {
        "title": "Data Engineer",
        "skills": ["Python", "SQL", "Airflow", "dbt", "Data Modeling"],
        "department": "Data",
        "location": "Remote (Americas)",
        "employment_type": "Full-time",
        "summary": (
            "Build trustworthy data pipelines that power analytics, reporting, and "
            "machine learning across the hiring lifecycle."
        ),
        "about": (
            "You will design batch and streaming pipelines that consolidate product, "
            "marketing, and operational data into reliable datasets. Data quality, "
            "lineage, and documentation are first-class concerns on this team."
        ),
        "responsibilities": [
            "Develop ETL/ELT pipelines with Airflow and transformation layers in dbt.",
            "Model warehouse tables for funnel analytics, recruiter activity, and ML features.",
            "Implement data quality checks, alerting, and schema evolution practices.",
            "Partner with analysts and ML engineers on dataset requirements and SLAs.",
            "Optimize query performance and pipeline cost as data volume grows.",
        ],
        "requirements": [
            "3+ years building production data pipelines.",
            "Advanced SQL skills and solid dimensional modeling fundamentals.",
            "Strong Python for orchestration, tooling, and pipeline maintenance.",
            "Experience with modern warehouse platforms such as Snowflake, BigQuery, or Redshift.",
            "Attention to documentation, ownership, and on-call hygiene for data systems.",
        ],
        "nice_to_have": [
            "Experience with Kafka, Debezium, or change-data-capture patterns.",
            "Familiarity with privacy-aware data handling and PII tokenization.",
            "Exposure to feature store or ML training dataset pipelines.",
        ],
    },
    {
        "title": "UX Researcher",
        "skills": ["User Interviews", "Usability Testing", "Survey Design", "Synthesis", "Stakeholder Communication"],
        "department": "Design",
        "location": "Remote (US & EU)",
        "employment_type": "Full-time",
        "summary": (
            "Bring the voice of recruiters and candidates into product decisions "
            "through rigorous, actionable research."
        ),
        "about": (
            "You will plan and execute mixed-methods research across the hiring funnel, "
            "from job discovery to application status transparency. Your insights will "
            "directly influence roadmap priorities and design direction."
        ),
        "responsibilities": [
            "Plan research studies with clear goals, methods, and recruitment strategies.",
            "Conduct interviews, moderated usability sessions, and survey-based studies.",
            "Synthesize findings into journey maps, personas, and opportunity frameworks.",
            "Present actionable recommendations to product, design, and leadership.",
            "Build a research repository and advocate for continuous discovery practices.",
        ],
        "requirements": [
            "3+ years UX research experience in product-led organizations.",
            "Portfolio or case studies showing impact on shipped product decisions.",
            "Strong facilitation skills and neutral, inclusive interviewing technique.",
            "Ability to size research efforts appropriately for startup pace.",
            "Excellent storytelling that connects evidence to recommended next steps.",
        ],
        "nice_to_have": [
            "Experience researching B2B admin tools or multi-sided marketplaces.",
            "Familiarity with tools like Dovetail, UserTesting, or Lookback.",
            "Background in accessibility research or inclusive design methods.",
        ],
    },
    {
        "title": "Platform Engineer",
        "skills": ["Go", "Kubernetes", "Internal Developer Platforms", "APIs", "Developer Experience"],
        "department": "Platform",
        "location": "Remote (Global)",
        "employment_type": "Full-time",
        "summary": (
            "Build internal platform capabilities that help product engineers ship "
            "faster with golden paths for services, environments, and observability."
        ),
        "about": (
            "Platform engineering at HireLens means treating internal developers as "
            "customers. You will create self-service tooling, templates, and paved-road "
            "workflows that reduce cognitive load and operational toil."
        ),
        "responsibilities": [
            "Develop internal APIs and CLIs for service scaffolding and environment provisioning.",
            "Maintain Kubernetes abstractions, deployment charts, and service templates.",
            "Improve developer onboarding with documentation, examples, and office hours.",
            "Measure platform adoption and iterate based on engineer feedback.",
            "Collaborate with SRE and security on safe defaults and policy enforcement.",
        ],
        "requirements": [
            "4+ years software engineering with platform or infrastructure focus.",
            "Strong backend skills in Go, Python, or similar systems languages.",
            "Experience operating Kubernetes clusters and containerized services.",
            "Product mindset for internal tools with empathy for developer workflows.",
            "Clear documentation habits and comfort presenting at engineering forums.",
        ],
        "nice_to_have": [
            "Experience with Backstage, Crossplane, or internal developer portal tools.",
            "Background building CI templates or reusable GitHub/GitLab workflows.",
            "Familiarity with service catalog and ownership metadata practices.",
        ],
    },
    {
        "title": "Android Developer",
        "skills": ["Kotlin", "Jetpack Compose", "Android SDK", "REST APIs", "Material Design"],
        "department": "Engineering",
        "location": "Remote (EU)",
        "employment_type": "Full-time",
        "summary": (
            "Deliver a polished Android app that helps recruiting teams stay responsive "
            "to candidates wherever they work."
        ),
        "about": (
            "You will own the Android codebase alongside our iOS initiative, focusing "
            "on recruiter workflows first. We value modern Kotlin patterns, thoughtful "
            "offline behavior, and performance on a wide range of devices."
        ),
        "responsibilities": [
            "Build features with Jetpack Compose, ViewModel, and coroutine-based architecture.",
            "Integrate authentication, push notifications, and secure local storage.",
            "Write unit and instrumentation tests for critical user journeys.",
            "Collaborate with design to implement Material Design 3 patterns.",
            "Manage Play Store releases, staged rollouts, and crash triage.",
        ],
        "requirements": [
            "4+ years professional Android development experience.",
            "Strong Kotlin skills and familiarity with modern Android architecture components.",
            "Experience consuming REST APIs and handling pagination, caching, and errors.",
            "Understanding of Android security basics for stored credentials and networking.",
            "Comfort profiling memory, startup time, and UI jank issues.",
        ],
        "nice_to_have": [
            "Experience with WorkManager, Room, or encrypted shared preferences.",
            "Background in enterprise or productivity Android applications.",
            "Familiarity with Firebase Crashlytics or similar mobile observability tools.",
        ],
    },
    {
        "title": "Customer Success Engineer",
        "skills": ["Technical Support", "SQL", "APIs", "Onboarding", "Customer Communication"],
        "department": "Customer Success",
        "location": "Remote (US)",
        "employment_type": "Full-time",
        "summary": (
            "Help enterprise customers adopt HireLens successfully by combining "
            "technical troubleshooting with proactive implementation guidance."
        ),
        "about": (
            "You sit at the intersection of support, solutions engineering, and account "
            "health. You will debug integrations, configure workflows, and translate "
            "customer feedback into actionable product input."
        ),
        "responsibilities": [
            "Lead technical onboarding for new customers and ensure time-to-value milestones.",
            "Troubleshoot API, SSO, and data import issues with clear customer communication.",
            "Create runbooks, office hours, and training materials for common workflows.",
            "Monitor account health signals and escalate risks with account managers.",
            "Partner with product and engineering on recurring customer pain points.",
        ],
        "requirements": [
            "3+ years in customer success, solutions engineering, or technical support.",
            "Ability to read logs, trace API requests, and write basic SQL queries.",
            "Excellent written and verbal communication with technical and business audiences.",
            "Organized approach to ticket management and follow-through.",
            "Empathy for users under deadline pressure during hiring cycles.",
        ],
        "nice_to_have": [
            "Experience with HRIS or ATS integrations.",
            "Background in SaaS admin configuration and RBAC setups.",
            "Familiarity with tools like Zendesk, Intercom, or Gainsight.",
        ],
    },
    {
        "title": "Technical Writer",
        "skills": ["Documentation", "Markdown", "API Docs", "Information Architecture", "Developer Education"],
        "department": "Product",
        "location": "Remote (Global)",
        "employment_type": "Full-time",
        "summary": (
            "Create clear documentation for recruiters, candidates, and developers "
            "integrating with the HireLens platform."
        ),
        "about": (
            "Great docs reduce support load and accelerate adoption. You will own "
            "help center content, API references, release notes, and internal playbooks "
            "with consistent voice and strong information architecture."
        ),
        "responsibilities": [
            "Write and maintain user guides for job posting, application review, and admin setup.",
            "Document public APIs with accurate examples, auth flows, and error references.",
            "Partner with engineering on docs-as-code workflows and review processes.",
            "Audit existing content for accuracy, gaps, and outdated screenshots.",
            "Establish style guides, templates, and content governance practices.",
        ],
        "requirements": [
            "3+ years technical writing experience for software products.",
            "Excellent command of English and ability to simplify complex workflows.",
            "Proficiency with Markdown, docs tooling, and diagramming for architecture overviews.",
            "Comfort interviewing engineers and validating docs against real product behavior.",
            "Strong attention to structure, searchability, and version alignment with releases.",
        ],
        "nice_to_have": [
            "Experience documenting REST APIs with OpenAPI or similar standards.",
            "Background in HR tech, developer tools, or B2B SaaS onboarding content.",
            "Familiarity with static site generators or docs platforms like MkDocs or ReadMe.",
        ],
    },
]
