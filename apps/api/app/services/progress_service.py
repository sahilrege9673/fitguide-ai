import io
import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime, date, timedelta, timezone

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, KeepTogether, HRFlowable
)

from app.schemas.progress import (
    ProgressSummaryResponse, DailyActivity, MuscleGroupVolume, TimeframeEnum
)
from app.services.workout_service import _SESSIONS_STORE, _SCHEDULE_STORE
from app.services.profile_service import ProfileService
from app.core.config import settings
import httpx

logger = logging.getLogger(__name__)

# Urban Performance Palette for ReportLab
COLOR_CARBON = colors.HexColor("#171B18")
COLOR_FOREST = colors.HexColor("#26372D")
COLOR_LIME = colors.HexColor("#C4E76B")
COLOR_CHALK = colors.HexColor("#E8E5D9")
COLOR_SAND = colors.HexColor("#B5A78D")
COLOR_ORANGE = colors.HexColor("#C8794D")
COLOR_LIGHT_BG = colors.HexColor("#F4F3EF")
COLOR_DARK_TEXT = colors.HexColor("#171B18")
COLOR_MUTED_BORDER = colors.HexColor("#D8D5CA")

MUSCLE_DISPLAY_NAMES = {
    "chest": "Chest / Pectorals",
    "anterior_deltoids": "Shoulders (Anterior)",
    "lateral_deltoids": "Shoulders (Lateral)",
    "posterior_deltoids": "Shoulders (Posterior)",
    "lats": "Back / Latissimus",
    "rhomboids": "Upper Back / Rhomboids",
    "quadriceps": "Quadriceps",
    "hamstrings": "Hamstrings",
    "glutes": "Glutes",
    "calves": "Calves",
    "triceps": "Triceps",
    "biceps": "Biceps",
    "core": "Core / Abdominals",
    "cardiovascular": "Cardiovascular Conditioning",
    "mobility": "Mobility & Joint Health"
}

class ProgressService:
    @classmethod
    def _parse_timeframe_days(cls, timeframe: str) -> int:
        if timeframe == "7d":
            return 7
        elif timeframe == "30d":
            return 30
        elif timeframe == "90d":
            return 90
        elif timeframe == "all":
            return 180
        return 30

    @classmethod
    def calculate_summary(cls, user_id: UUID, timeframe: str = "30d") -> ProgressSummaryResponse:
        days_count = cls._parse_timeframe_days(timeframe)
        today = date.today()
        start_date = today - timedelta(days=days_count - 1)
        end_date = today

        # Fetch sessions for user
        user_sessions = [
            s for s in _SESSIONS_STORE.values()
            if s.get("user_id") == user_id
        ]

        # Calculate scheduled workouts in window
        user_schedule = _SCHEDULE_STORE.get(user_id, [])
        scheduled_in_window = [
            entry for entry in user_schedule
            if start_date <= entry.get("scheduled_date", date.min) <= end_date
            and not entry.get("is_rest_day", False)
        ]
        scheduled_count = len(scheduled_in_window)

        # Filter completed sessions within date window
        completed_sessions = []
        for s in user_sessions:
            if s.get("status") == "completed":
                comp_dt = s.get("completed_at")
                if comp_dt:
                    comp_date = comp_dt.date() if isinstance(comp_dt, datetime) else comp_dt
                    if start_date <= comp_date <= end_date:
                        completed_sessions.append(s)

        completed_count = len(completed_sessions)

        # Base consistency calculation
        if scheduled_count > 0:
            consistency = min(100.0, round((completed_count / scheduled_count) * 100.0, 1))
        elif completed_count > 0:
            consistency = 100.0
        else:
            consistency = 0.0

        # Calculate volume, active minutes, reps, sets, and muscle distribution
        total_volume_kg = 0.0
        total_active_mins = 0
        total_reps = 0
        total_sets = 0
        muscle_sets_map: Dict[str, int] = {}
        muscle_vol_map: Dict[str, float] = {}

        # Track completed dates for streak
        completed_dates_set = set()

        for s in completed_sessions:
            dur = s.get("actual_duration_mins") or s.get("planned_duration_mins") or 45
            total_active_mins += dur

            comp_dt = s.get("completed_at")
            if comp_dt:
                comp_date = comp_dt.date() if isinstance(comp_dt, datetime) else comp_dt
                completed_dates_set.add(comp_date)

            for ex_item in s.get("exercises", []):
                ex_data = ex_item.get("exercise")
                muscle = "core"
                if ex_data:
                    if hasattr(ex_data, "muscle_group"):
                        muscle = ex_data.muscle_group
                    elif isinstance(ex_data, dict):
                        muscle = ex_data.get("muscle_group", "core")

                logs = ex_item.get("logs", [])
                if logs:
                    for log in logs:
                        reps = log.get("reps_performed") or log.get("reps_completed") or 0
                        weight = log.get("weight_kg", 0.0)
                        total_reps += reps
                        total_sets += 1
                        vol = reps * (weight if weight > 0 else 1.0)
                        total_volume_kg += vol
                        muscle_sets_map[muscle] = muscle_sets_map.get(muscle, 0) + 1
                        muscle_vol_map[muscle] = muscle_vol_map.get(muscle, 0.0) + vol
                elif ex_item.get("is_completed", False):
                    # In case session completed without individual set logs
                    t_sets = ex_item.get("target_sets", 3)
                    total_sets += t_sets
                    total_reps += t_sets * 10
                    vol = t_sets * 10 * 20.0
                    total_volume_kg += vol
                    muscle_sets_map[muscle] = muscle_sets_map.get(muscle, 0) + t_sets
                    muscle_vol_map[muscle] = muscle_vol_map.get(muscle, 0.0) + vol

        # Compute current streak
        streak_days = 0
        check_date = today
        while check_date in completed_dates_set:
            streak_days += 1
            check_date -= timedelta(days=1)

        # If today wasn't completed yet, check if yesterday was completed to keep active streak
        if streak_days == 0 and (today - timedelta(days=1)) in completed_dates_set:
            check_date = today - timedelta(days=1)
            while check_date in completed_dates_set:
                streak_days += 1
                check_date -= timedelta(days=1)

        # Format muscle group distribution
        muscle_distribution: List[MuscleGroupVolume] = []
        for muscle, sets in sorted(muscle_sets_map.items(), key=lambda x: x[1], reverse=True):
            pct = round((sets / max(1, total_sets)) * 100.0, 1)
            muscle_distribution.append(MuscleGroupVolume(
                muscle_group=muscle,
                display_name=MUSCLE_DISPLAY_NAMES.get(muscle, muscle.replace("_", " ").title()),
                sets=sets,
                volume_kg=round(muscle_vol_map.get(muscle, 0.0), 1),
                percentage=pct
            ))

        # Format daily activity trend for chart
        daily_activity: List[DailyActivity] = []
        # For display, show last 7 days or up to 14 days depending on timeframe
        display_days = min(days_count, 14 if days_count <= 30 else 30)
        chart_start = today - timedelta(days=display_days - 1)

        for d_offset in range(display_days):
            cur_d = chart_start + timedelta(days=d_offset)
            d_str = cur_d.strftime("%Y-%m-%d")
            day_name = cur_d.strftime("%a")

            matching_completed = [
                s for s in completed_sessions
                if s.get("completed_at") and (
                    s["completed_at"].date() if isinstance(s["completed_at"], datetime) else s["completed_at"]
                ) == cur_d
            ]

            if matching_completed:
                first_s = matching_completed[0]
                d_vol = sum(
                    (l.get("reps_performed") or l.get("reps_completed") or 0) * (l.get("weight_kg", 0.0) or 1.0)
                    for se in first_s.get("exercises", [])
                    for l in se.get("logs", [])
                )
                d_sets = sum(len(se.get("logs", [])) for se in first_s.get("exercises", []))
                d_mins = first_s.get("actual_duration_mins") or first_s.get("planned_duration_mins") or 45

                daily_activity.append(DailyActivity(
                    date=d_str,
                    day_name=day_name,
                    completed=True,
                    workout_title=first_s.get("title", "Training Session"),
                    active_mins=d_mins,
                    volume_kg=round(d_vol, 1),
                    sets_count=d_sets
                ))
            else:
                daily_activity.append(DailyActivity(
                    date=d_str,
                    day_name=day_name,
                    completed=False,
                    workout_title=None,
                    active_mins=0,
                    volume_kg=0.0,
                    sets_count=0
                ))

        # Generate Grounded AI Insights
        ai_insights = cls._generate_insights(
            timeframe=timeframe,
            consistency=consistency,
            completed_count=completed_count,
            scheduled_count=scheduled_count,
            total_vol=total_volume_kg,
            total_mins=total_active_mins,
            streak=streak_days,
            muscles=muscle_distribution,
            user_id=user_id
        )

        return ProgressSummaryResponse(
            timeframe=timeframe,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            consistency_percentage=consistency,
            completed_workouts=completed_count,
            scheduled_workouts=scheduled_count,
            total_volume_kg=round(total_volume_kg, 1),
            total_active_mins=total_active_mins,
            total_reps=total_reps,
            total_sets=total_sets,
            streak_days=streak_days,
            muscle_group_distribution=muscle_distribution,
            daily_activity=daily_activity,
            ai_insights=ai_insights,
            generated_at=datetime.now(timezone.utc)
        )

    @classmethod
    def _generate_insights(
        cls,
        timeframe: str,
        consistency: float,
        completed_count: int,
        scheduled_count: int,
        total_vol: float,
        total_mins: int,
        streak: int,
        muscles: List[MuscleGroupVolume],
        user_id: UUID
    ) -> str:
        """Generates grounded athletic coach insights based on real volume and consistency."""
        prefs = ProfileService.get_preferences(user_id)
        age_group = prefs.age_group if prefs else "adult_18_64"
        goals = prefs.fitness_goals if prefs else ["general_fitness"]

        # If user has completed workouts, provide quantitative progressive overload feedback
        if completed_count > 0:
            top_muscles = [m.display_name for m in muscles[:2]] if muscles else ["Primary Movers"]
            muscle_str = " and ".join(top_muscles)

            if consistency >= 80.0:
                consistency_comment = f"Exceptional training compliance at {consistency}%. You are maintaining the neuromuscular stimulus required for progressive overload and adaptations."
            elif consistency >= 50.0:
                consistency_comment = f"Solid foundation at {consistency}% consistency. Prioritize scheduled sessions to preserve weekly volume thresholds."
            else:
                consistency_comment = f"Current consistency is {consistency}%. Focusing on 2-3 committed sessions per week will compound neuromuscular improvements."

            insights = (
                f"**Biomechanical Volume Review ({timeframe.upper()})**: Over the selected period, you accumulated "
                f"**{round(total_vol):,} kg** of total volume load across **{completed_count} sessions** ({total_mins} total active minutes). "
                f"Your training stimulus has emphasized **{muscle_str}**, aligning with your focus on {', '.join(goals).replace('_', ' ')}. "
                f"\n\n**Recovery & Consistency**: {consistency_comment} Your current streak stands at **{streak} day(s)**. "
                f"For the upcoming cycle, ensure progressive overload by incrementally increasing either repetitions or external load by 2.5–5% while maintaining strict eccentric tempo."
            )
        else:
            insights = (
                f"**Initial Training Phase**: No completed sessions have been logged yet for the {timeframe.upper()} cycle. "
                f"Your weekly plan has been calibrated for **{age_group.replace('_', ' ')}** focusing on **{', '.join(goals).replace('_', ' ')}**. "
                f"Begin your first scheduled session to initialize neuromuscular baselines, set tracking, and workload metrics."
            )

        return insights

    @classmethod
    def generate_pdf_report(cls, user_id: UUID, timeframe: str = "30d") -> bytes:
        """
        Builds and renders an authentic, publication-grade PDF activity report using ReportLab.
        Adheres to Urban Performance design aesthetics (Carbon, Forest, Lime, Sand, Chalk).
        """
        summary = cls.calculate_summary(user_id, timeframe)
        prefs = ProfileService.get_preferences(user_id)
        profile = ProfileService.get_profile(user_id)

        user_name = profile.full_name or profile.email if profile else "Athlete"
        age_group = (prefs.age_group if prefs else "adult_18_64").replace("_", " ").title()
        goals_str = ", ".join(prefs.fitness_goals if prefs else ["General Athleticism"]).replace("_", " ").title()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom Typography Styles
        style_header_brand = ParagraphStyle(
            name="BrandHeader",
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=COLOR_CHALK
        )
        style_header_sub = ParagraphStyle(
            name="BrandSub",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=COLOR_LIME
        )
        style_section_title = ParagraphStyle(
            name="SectionTitle",
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=COLOR_CARBON
        )
        style_kpi_value = ParagraphStyle(
            name="KPIValue",
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=18,
            textColor=COLOR_CARBON,
            alignment=1 # Center
        )
        style_kpi_label = ParagraphStyle(
            name="KPILabel",
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=COLOR_SAND,
            alignment=1 # Center
        )
        style_table_header = ParagraphStyle(
            name="TableHeader",
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=COLOR_CHALK
        )
        style_table_cell = ParagraphStyle(
            name="TableCell",
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=COLOR_CARBON
        )
        style_table_cell_bold = ParagraphStyle(
            name="TableCellBold",
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=11,
            textColor=COLOR_CARBON
        )
        style_body_text = ParagraphStyle(
            name="BodyTextCustom",
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=COLOR_CARBON
        )
        style_disclaimer = ParagraphStyle(
            name="Disclaimer",
            fontName="Helvetica-Oblique",
            fontSize=7,
            leading=9,
            textColor=COLOR_SAND,
            alignment=1 # Center
        )

        story = []

        # 1. ATHLETIC HEADER BANNER
        header_table_data = [
            [
                Paragraph("<b>FEEDGUIDE AI</b> | PERFORMANCE REPORT", style_header_brand),
                Paragraph(f"ATHLETE: <b>{user_name.upper()}</b><br/>WINDOW: <b>{summary.start_date} → {summary.end_date}</b>", style_header_sub)
            ]
        ]
        header_table = Table(header_table_data, colWidths=[340, 200])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLOR_CARBON),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 14),
            ('RIGHTPADDING', (0, 0), (-1, -1), 14),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 14))

        # 2. ATHLETE CONTEXT SUB-STRIP
        context_data = [
            [
                Paragraph(f"<b>AGE GROUP:</b> {age_group}", style_table_cell),
                Paragraph(f"<b>GOALS:</b> {goals_str}", style_table_cell),
                Paragraph(f"<b>TIMEFRAME:</b> {timeframe.upper()}", style_table_cell),
                Paragraph(f"<b>GENERATED:</b> {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", style_table_cell)
            ]
        ]
        context_table = Table(context_data, colWidths=[135, 175, 100, 130])
        context_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLOR_LIGHT_BG),
            ('BOX', (0, 0), (-1, -1), 0.5, COLOR_MUTED_BORDER),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(context_table)
        story.append(Spacer(1, 14))

        # 3. EXECUTIVE KPI CARDS GRID (1x5)
        kpi_data = [
            [
                Paragraph(f"<b>{summary.consistency_percentage}%</b>", style_kpi_value),
                Paragraph(f"<b>{summary.completed_workouts}</b>", style_kpi_value),
                Paragraph(f"<b>{round(summary.total_volume_kg):,}</b>", style_kpi_value),
                Paragraph(f"<b>{summary.total_active_mins}m</b>", style_kpi_value),
                Paragraph(f"<b>{summary.streak_days}d</b>", style_kpi_value),
            ],
            [
                Paragraph("CONSISTENCY", style_kpi_label),
                Paragraph("COMPLETED", style_kpi_label),
                Paragraph("TOTAL VOLUME (KG)", style_kpi_label),
                Paragraph("ACTIVE TIME", style_kpi_label),
                Paragraph("STREAK", style_kpi_label),
            ]
        ]
        kpi_table = Table(kpi_data, colWidths=[108, 108, 108, 108, 108])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('BOX', (0, 0), (-1, -1), 1, COLOR_CARBON),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_MUTED_BORDER),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
            ('TOPPADDING', (0, 1), (-1, 1), 2),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 8),
            ('LINEBELOW', (0, 0), (-1, 0), 2, COLOR_LIME),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 16))

        # 4. TRAINING VOLUME & MUSCLE GROUP BREAKDOWN
        story.append(Paragraph("<b>VOLUME BY MUSCLE GROUP</b>", style_section_title))
        story.append(Spacer(1, 6))

        muscle_rows = [
            [
                Paragraph("MUSCLE GROUP / ANATOMICAL REGION", style_table_header),
                Paragraph("WORKING SETS", style_table_header),
                Paragraph("VOLUME LOAD (KG)", style_table_header),
                Paragraph("SHARE %", style_table_header)
            ]
        ]

        if summary.muscle_group_distribution:
            for item in summary.muscle_group_distribution[:6]:
                muscle_rows.append([
                    Paragraph(item.display_name, style_table_cell_bold),
                    Paragraph(str(item.sets), style_table_cell),
                    Paragraph(f"{round(item.volume_kg):,} kg", style_table_cell),
                    Paragraph(f"{item.percentage}%", style_table_cell)
                ])
        else:
            muscle_rows.append([
                Paragraph("Baseline Plan Initialized", style_table_cell),
                Paragraph("0", style_table_cell),
                Paragraph("0 kg", style_table_cell),
                Paragraph("0.0%", style_table_cell)
            ])

        muscle_table = Table(muscle_rows, colWidths=[240, 100, 110, 90])
        muscle_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_FOREST),
            ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_CHALK),
            ('GRID', (0, 0), (-1, -1), 0.5, COLOR_MUTED_BORDER),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_LIGHT_BG]),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(muscle_table)
        story.append(Spacer(1, 16))

        # 5. RECENT ACTIVITY LOG
        story.append(Paragraph("<b>RECENT COMPLETED SESSIONS</b>", style_section_title))
        story.append(Spacer(1, 6))

        activity_rows = [
            [
                Paragraph("DATE", style_table_header),
                Paragraph("SESSION TITLE", style_table_header),
                Paragraph("ACTIVE MINS", style_table_header),
                Paragraph("SETS", style_table_header),
                Paragraph("VOLUME (KG)", style_table_header)
            ]
        ]

        active_logged_days = [a for a in summary.daily_activity if a.completed]
        if active_logged_days:
            for act in active_logged_days[:5]:
                activity_rows.append([
                    Paragraph(act.date, style_table_cell_bold),
                    Paragraph(act.workout_title or "Strength Routine", style_table_cell),
                    Paragraph(f"{act.active_mins}m", style_table_cell),
                    Paragraph(str(act.sets_count), style_table_cell),
                    Paragraph(f"{round(act.volume_kg):,} kg", style_table_cell)
                ])
        else:
            activity_rows.append([
                Paragraph(summary.start_date, style_table_cell),
                Paragraph("No completed sessions recorded in selected timeframe", style_table_cell),
                Paragraph("0m", style_table_cell),
                Paragraph("0", style_table_cell),
                Paragraph("0 kg", style_table_cell)
            ])

        activity_table = Table(activity_rows, colWidths=[80, 240, 75, 55, 90])
        activity_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_CARBON),
            ('GRID', (0, 0), (-1, -1), 0.5, COLOR_MUTED_BORDER),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_LIGHT_BG]),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(activity_table)
        story.append(Spacer(1, 16))

        # 6. GROUNDED AI ATHLETIC COACH EVALUATION
        story.append(Paragraph("<b>AI ATHLETIC COACH ANALYSIS</b>", style_section_title))
        story.append(Spacer(1, 6))

        # Clean markdown bolding for reportlab paragraph
        clean_insights = summary.ai_insights.replace("**", "<b>", 1)
        while "**" in clean_insights:
            clean_insights = clean_insights.replace("**", "</b>", 1)
            if "**" in clean_insights:
                clean_insights = clean_insights.replace("**", "<b>", 1)
        clean_insights = clean_insights.replace("\n\n", "<br/><br/>")

        coach_data = [
            [
                Paragraph(f"<font color='#C4E76B'><b>ANALYSIS:</b></font><br/>{clean_insights}", style_body_text)
            ]
        ]
        coach_table = Table(coach_data, colWidths=[540])
        coach_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLOR_LIGHT_BG),
            ('BOX', (0, 0), (-1, -1), 1, COLOR_FOREST),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('LINELEFT', (0, 0), (-1, -1), 4, COLOR_LIME),
        ]))
        story.append(coach_table)
        story.append(Spacer(1, 18))

        # 7. SAFETY & MEDICAL DISCLAIMER
        disclaimer_text = (
            "SAFETY & MEDICAL NOTICE: FeedGuide AI is an educational fitness and athletic companion, not a licensed medical provider. "
            "Data in this report represents recorded workout telemetry. Consult a physician before beginning any new training program. "
            "Never train through acute pain, dizziness, or cardiac distress."
        )
        story.append(Paragraph(disclaimer_text, style_disclaimer))

        # Build document
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
