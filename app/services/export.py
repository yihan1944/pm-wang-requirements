"""Export project analysis to Markdown."""

from sqlalchemy.orm import Session

from app.models.project import Project


def export_project_markdown(project: Project, db: Session) -> str:
    """Render the full analysis as a Markdown document following the methodology template."""
    lines = [f"# {project.name} — C端消费者需求分析\n"]

    if project.description:
        lines.append(f"> {project.description}\n")

    # Section 0: Research
    lines.append("---\n")
    lines.append("## 〇、研究说明\n")
    if project.research_methods:
        lines.append("### 研究方法与数据来源\n")
        lines.append(project.research_methods + "\n")
    if project.scoring_anchors:
        lines.append("### 评分锚点定义\n")
        lines.append(project.scoring_anchors + "\n")

    # Section 1: Who
    lines.append("---\n")
    lines.append("## 一、用户（Who）\n")
    for p in project.user_profiles:
        if p.target_user:
            lines.append(f"### 目标用户\n{p.target_user}\n")
        lines.append("### 用户画像\n")
        lines.append("| 维度 | 内容 | 证据 | 状态 |")
        lines.append("|------|------|------|------|")
        for dim, field in [
            ("年龄", p.age), ("性别", p.gender), ("职业", p.occupation),
            ("收入", p.income), ("地域", p.region), ("数字化能力", p.digital_ability),
            ("消费能力", p.spending_power), ("典型特征", p.typical_traits),
        ]:
            if field:
                lines.append(f"| {dim} | {field} | {p.evidence or ''} | {p.status} |")
        lines.append("")

    if project.user_segments:
        lines.append("### 用户分层\n")
        lines.append("| 用户类型 | 特征 | 占比 | 优先级 | 证据 |")
        lines.append("|----------|------|------|--------|------|")
        for s in project.user_segments:
            lines.append(f"| {s.user_type} | {s.traits or ''} | {s.proportion or ''} | {s.priority or ''} | {s.evidence or ''} |")
        lines.append("")

    # Section 2: Scene
    lines.append("---\n")
    lines.append("## 二、场景（Scene）\n")
    if project.scenarios:
        lines.append("### 核心使用场景\n")
        lines.append("| 场景名称 | 时间 | 地点 | 触发事件 | 频率 |")
        lines.append("|----------|------|------|----------|------|")
        for s in project.scenarios:
            lines.append(f"| {s.name} | {s.time_desc or ''} | {s.location or ''} | {s.trigger_event or ''} | {s.frequency or ''} |")
        lines.append("")

    if project.behavior_paths:
        lines.append("### 用户行为路径\n")
        lines.append("| 顺序 | 路径节点 | 流失风险 | 替代动作 |")
        lines.append("|------|----------|----------|----------|")
        for p in sorted(project.behavior_paths, key=lambda x: x.step_order):
            lines.append(f"| {p.step_order} | {p.step_name} | {p.churn_risk or ''} | {p.alternative_actions or ''} |")
        lines.append("")

    # Section 3: Job
    lines.append("---\n")
    lines.append("## 三、动机（Job）\n")
    if project.jobs:
        lines.append("### JTBD\n")
        for j in project.jobs:
            lines.append(f"> 当 **{j.when or '___'}** 的时候，")
            lines.append(f"> 我希望 **{j.i_want or '___'}**，")
            lines.append(f"> 从而能够 **{j.so_that or '___'}**。\n")

    if project.user_goals:
        lines.append("### 用户核心目标\n")
        lines.append("| 优先级 | 目标 | 证据 |")
        lines.append("|--------|------|------|")
        for g in project.user_goals:
            lines.append(f"| {g.priority} | {g.goal} | {g.evidence or ''} |")
        lines.append("")

    if project.need_classifications:
        lines.append("### 需求分类\n")
        lines.append("| 类型 | 内容 |")
        lines.append("|------|------|")
        for n in project.need_classifications:
            lines.append(f"| {n.need_type} | {n.content} |")
        lines.append("")

    # Section 4: Pain
    lines.append("---\n")
    lines.append("## 四、痛点（Pain）\n")
    if project.pain_points:
        lines.append("### 用户痛点\n")
        lines.append("| 流程阶段 | 当前行为 | 问题 | 严重程度 | 发生频率 | 状态 |")
        lines.append("|----------|----------|------|----------|----------|------|")
        for p in project.pain_points:
            lines.append(f"| {p.flow_stage or ''} | {p.current_behavior or ''} | {p.problem or ''} | {p.severity} | {p.frequency} | {p.status} |")
        lines.append("")

    if project.competitors:
        lines.append("### 竞品与替代方案\n")
        lines.append("| 替代方案 | 解决方式 | 优势 | 局限 | 满意度 |")
        lines.append("|----------|----------|------|------|--------|")
        for c in project.competitors:
            lines.append(f"| {c.name} | {c.solution or ''} | {c.advantages or ''} | {c.limitations or ''} | {c.satisfaction or ''} |")
        lines.append("")

    if project.unmet_needs:
        lines.append("### 未满足需求\n")
        lines.append("| 需求 | 当前替代方案 | 满足程度 | 证据 |")
        lines.append("|------|--------------|----------|------|")
        for u in project.unmet_needs:
            lines.append(f"| {u.need} | {u.current_alternative or ''} | {u.satisfaction} | {u.evidence or ''} |")
        lines.append("")

    # Section 5: Insight
    lines.append("---\n")
    lines.append("## 五、洞察（Insight）\n")
    if project.insights:
        lines.append("| 洞察 | 支撑痛点 | 含义 | 状态 |")
        lines.append("|------|----------|------|------|")
        for i in project.insights:
            lines.append(f"| {i.insight} | {i.supporting_pains or ''} | {i.meaning or ''} | {i.status} |")
        lines.append("")

    # Section 6: Opportunity
    lines.append("---\n")
    lines.append("## 六、机会（Opportunity）\n")
    if project.opportunities:
        lines.append("### 产品机会点\n")
        lines.append("| 机会点 | 来源洞察 | 对应痛点 | 用户价值 | 商业价值 | 优先级 | 状态 |")
        lines.append("|--------|----------|----------|----------|----------|--------|------|")
        for o in project.opportunities:
            lines.append(f"| {o.opportunity} | {o.source_insight or ''} | {o.related_pain or ''} | {o.user_value} | {o.business_value} | {o.priority} | {o.status} |")
        lines.append("")

    if project.capabilities:
        lines.append("### 产品能力建议\n")
        lines.append("| 方向 | 建议方案 |")
        lines.append("|------|----------|")
        for c in project.capabilities:
            lines.append(f"| {c.direction} | {c.suggestion} |")
        lines.append("")

    if project.mvp_items:
        lines.append("### MVP建议\n")
        lines.append("| 功能 | 目标 | 验证指标 |")
        lines.append("|------|------|----------|")
        for m in project.mvp_items:
            lines.append(f"| {m.feature} | {m.goal or ''} | {m.validation_metric or ''} |")
        lines.append("")

    # Section 7: Requirement
    lines.append("---\n")
    lines.append("## 需求说明\n")
    if project.requirement_docs:
        for doc in project.requirement_docs:
            header = f"### {doc.section}"
            if doc.subsection:
                header += f" — {doc.subsection}"
            lines.append(header + "\n")
            lines.append(doc.content + "\n")

    return "\n".join(lines)
