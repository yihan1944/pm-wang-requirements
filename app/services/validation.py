"""Completeness and quality validation for analysis projects."""

from sqlalchemy.orm import Session

from app.models.project import Project


def get_project_completion(project: Project, db: Session) -> dict:
    """Calculate completion status for each section of the analysis."""
    sections = {}

    # Section 0: Research
    has_research = bool(project.research_methods or project.scoring_anchors)
    sections["research"] = {
        "label": "研究说明",
        "complete": has_research,
        "items": _count_items(has_research, 1),
        "issues": [] if has_research else ["未填写研究方法或评分锚点"],
    }

    # Section 1: Who
    profiles = project.user_profiles
    segments = project.user_segments
    who_total = len(profiles) + len(segments)
    who_issues = []
    for p in profiles:
        if p.status not in ("已验证", "待验证", "假设"):
            who_issues.append(f"用户画像 #{p.id} 缺少状态标注")
    sections["who"] = {
        "label": "用户 (Who)",
        "complete": who_total > 0 and not who_issues,
        "items": _count_items(who_total > 0, who_total),
        "issues": who_issues + (["未填写任何用户画像或分层"] if who_total == 0 else []),
    }

    # Section 2: Scene
    scenarios = project.scenarios
    paths = project.behavior_paths
    scene_total = len(scenarios) + len(paths)
    sections["scene"] = {
        "label": "场景 (Scene)",
        "complete": scene_total > 0,
        "items": _count_items(scene_total > 0, scene_total),
        "issues": [] if scene_total > 0 else ["未填写任何场景或行为路径"],
    }

    # Section 3: Job
    jobs = project.jobs
    goals = project.user_goals
    needs = project.need_classifications
    job_total = len(jobs) + len(goals) + len(needs)
    job_issues = []
    for g in goals:
        if g.priority not in ("P0", "P1", "P2"):
            job_issues.append(f"用户目标 #{g.id} 优先级未使用 P0/P1/P2")
    sections["job"] = {
        "label": "动机 (Job)",
        "complete": job_total > 0 and not job_issues,
        "items": _count_items(job_total > 0, job_total),
        "issues": job_issues + (["未填写任何 JTBD / 用户目标 / 需求分类"] if job_total == 0 else []),
    }

    # Section 4: Pain
    pains = project.pain_points
    competitors = project.competitors
    unmet = project.unmet_needs
    pain_total = len(pains) + len(competitors) + len(unmet)
    pain_issues = []
    for p in pains:
        if p.severity not in ("高", "中", "低"):
            pain_issues.append(f"痛点 #{p.id} 严重程度未使用高/中/低")
        if p.frequency not in ("高", "中", "低"):
            pain_issues.append(f"痛点 #{p.id} 发生频率未使用高/中/低")
        if p.status not in ("已验证", "待验证", "假设"):
            pain_issues.append(f"痛点 #{p.id} 缺少状态标注")
    sections["pain"] = {
        "label": "痛点 (Pain)",
        "complete": pain_total > 0 and not pain_issues,
        "items": _count_items(pain_total > 0, pain_total),
        "issues": pain_issues + (["未填写任何痛点 / 竞品 / 未满足需求"] if pain_total == 0 else []),
    }

    # Section 5: Insight
    insights = project.insights
    insight_issues = []
    for i in insights:
        if i.status not in ("已验证", "待验证", "假设"):
            insight_issues.append(f"洞察 #{i.id} 缺少状态标注")
    sections["insight"] = {
        "label": "洞察 (Insight)",
        "complete": len(insights) > 0 and not insight_issues,
        "items": _count_items(len(insights) > 0, len(insights)),
        "issues": insight_issues + (["未填写任何洞察"] if not insights else []),
    }

    # Section 6: Opportunity
    opps = project.opportunities
    caps = project.capabilities
    mvps = project.mvp_items
    opp_total = len(opps) + len(caps) + len(mvps)
    opp_issues = []
    for o in opps:
        if o.user_value not in ("高", "中", "低"):
            opp_issues.append(f"机会点 #{o.id} 用户价值未使用高/中/低")
        if o.business_value not in ("高", "中", "低"):
            opp_issues.append(f"机会点 #{o.id} 商业价值未使用高/中/低")
        if o.priority not in ("P0", "P1", "P2"):
            opp_issues.append(f"机会点 #{o.id} 优先级未使用 P0/P1/P2")
    sections["opportunity"] = {
        "label": "机会 (Opportunity)",
        "complete": opp_total > 0 and not opp_issues,
        "items": _count_items(opp_total > 0, opp_total),
        "issues": opp_issues + (["未填写任何机会点 / 能力建议 / MVP"] if opp_total == 0 else []),
    }

    # Section 7: Requirement
    reqs = project.requirement_docs
    sections["requirement"] = {
        "label": "需求说明",
        "complete": len(reqs) > 0,
        "items": _count_items(len(reqs) > 0, len(reqs)),
        "issues": [] if reqs else ["未填写需求说明"],
    }

    # Overall
    total_issues = sum(len(s["issues"]) for s in sections.values())
    complete_count = sum(1 for s in sections.values() if s["complete"])
    total_sections = len(sections)

    return {
        "sections": sections,
        "overall_complete": total_issues == 0,
        "complete_ratio": f"{complete_count}/{total_sections}",
        "complete_percent": round(complete_count / total_sections * 100) if total_sections else 0,
        "total_issues": total_issues,
    }


def _count_items(has_any: bool, count: int) -> str:
    if not has_any:
        return "未开始"
    return f"{count} 条"
