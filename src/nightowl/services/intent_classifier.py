class IntentClassifier:
    """Simple placeholder classifier; replace with LLM/tool based classifier later."""

    def classify(self, text: str) -> str:
        lowered = text.lower()
        if "other student" in lowered:
            return "other_student_query"
        if "attendance" in lowered or "absent" in lowered:
            return "attendance_query"
        if "announce" in lowered or "broadcast" in lowered:
            return "announcement_request"
        return "general_query"
