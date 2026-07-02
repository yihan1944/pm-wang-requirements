"""AI assist endpoint for generating user profiles and segments."""
import json
import os
import httpx
from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import Project

router = APIRouter()

AI_API_URL = os.getenv("AI_API_URL", "https://token-plan-cn.xiaomimimo.com/v1/chat/completions")
AI_API_KEY = os.getenv("AI_API_KEY", "")


class AiAssistRequest(BaseModel):
    prompt: str
    section: str  # who_profile, who_segment, scene, job, pain, insight, opportunity


SECTION_SCHEMAS = {
    "who_profile": """请根据用户的调研提示，生成一条用户画像 JSON，字段如下：
- target_user: 一句话描述目标用户
- age: 年龄（如 25-35）
- gender: 性别
- occupation: 职业
- income: 收入（如 15-25k）
- region: 地域
- digital_ability: 数字化能力（高/中/低）
- spending_power: 消费能力（高/中/低）
- typical_traits: 典型特征
- evidence: 证据/来源
- status: 假设

只输出 JSON，不要其他文字。""",
    "who_segment": """请根据用户的产品和调研提示，分析并生成一条用户分层 JSON，字段如下：
- user_type: 用户类型（核心用户/重要用户/潜在用户）
- traits: 该分层用户的核心特征描述（包括行为习惯、需求特点、使用场景等）
- proportion: 该分层在总用户中的占比估算（如 30%）
- priority: 优先级（P0/P1/P2，基于商业价值和实现难度）
- evidence: 证据/来源（支撑该分层判断的依据）

只输出 JSON，不要其他文字。""",
    "scene": """请根据用户的调研提示，生成一个使用场景 JSON，字段如下：
- name: 场景名称（如：通勤路上学习诗歌）
- time_desc: 时间描述
- location: 地点
- trigger_event: 触发事件
- frequency: 频率
- user_behavior: 用户行为
- user_goal: 用户目标

只输出 JSON，不要其他文字。""",
    "scene_with_user": """请根据用户的调研提示和用户画像，生成一个针对性的使用场景 JSON，字段如下：
- name: 场景名称
- time_desc: 时间描述
- location: 地点
- trigger_event: 触发事件
- frequency: 频率
- user_behavior: 用户行为
- user_goal: 用户目标

只输出 JSON，不要其他文字。""",
    "job": """请根据用户的调研提示，生成一个 JTBD（Jobs To Be Done）JSON，字段如下：
- when: 当___的时候（场景描述）
- i_want: 我希望___（用户想要做的事）
- so_that: 从而能够___（期望的结果）
- evidence: 证据/来源

只输出 JSON，不要其他文字。""",
    "pain": """请根据用户的调研提示，分析并生成一个用户痛点 JSON，字段如下：
- flow_stage: 流程阶段（用户在哪个环节遇到问题）
- current_behavior: 当前行为（用户目前怎么做）
- problem: 存在问题（核心痛点）
- severity: 严重程度（高/中/低）
- frequency: 发生频率（高/中/低）
- root_cause: 根本原因
- user_impact: 用户影响
- evidence: 证据/来源
- status: 假设

只输出 JSON，不要其他文字。""",
    "insight": """请根据用户的调研提示，生成一个洞察 JSON，字段如下：
- insight: 核心洞察（从痛点中提炼的关键判断）
- supporting_pains: 支撑痛点（引用痛点编号）
- meaning: 洞察含义（这个洞察意味着什么）
- status: 假设

只输出 JSON，不要其他文字。""",
    "opportunity": """请根据用户的调研提示，生成一个机会点 JSON，字段如下：
- opportunity: 机会点描述
- source_insight: 来源洞察（引用洞察编号）
- related_pain: 对应痛点
- user_value: 用户价值（高/中/低）
- business_value: 商业价值（高/中/低）
- priority: 优先级（P0/P1/P2）
- status: 假设

只输出 JSON，不要其他文字。""",
}


@router.post("/api/ai-assist")
async def ai_assist(req: AiAssistRequest, db: Session = Depends(get_db)):
    system_prompt = SECTION_SCHEMAS.get(req.section, SECTION_SCHEMAS["who_profile"])

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            AI_API_URL,
            headers={"Authorization": f"Bearer {AI_API_KEY}"},
            json={
                "model": "mimo-v2.5",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": req.prompt},
                ],
                "temperature": 0.7,
            },
        )
        data = resp.json()

    # Handle different API response formats
    if "choices" in data and len(data["choices"]) > 0:
        content = data["choices"][0]["message"]["content"]
    elif "message" in data:
        content = data["message"].get("content", "")
    elif "response" in data:
        content = data["response"]
    elif "content" in data:
        content = data["content"]
    else:
        # Return raw response for debugging
        return {"raw": str(data), "error": "无法解析AI响应"}

    # Extract JSON from response
    try:
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            result = json.loads(content[start:end])
        else:
            result = {"raw": content}
    except json.JSONDecodeError:
        result = {"raw": content}

    return result
