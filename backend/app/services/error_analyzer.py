from app.database import db


class ErrorAnalyzer:
    """
    Analyzes a student's error patterns to inform task generation.
    """

    def analyze_user_errors(self, user_id: int) -> dict:
        """
        Calculate an error profile from the user's evaluation history.

        Returns a dict mapping error_type -> error_rate (0.0 – 1.0).
        """
        return db.get_user_error_profile(user_id)

    def get_priority_focus_areas(self, error_profile: dict, top_n: int = 3) -> list:
        """
        Return the top-N error types the student should focus on.
        """
        sorted_errors = sorted(
            error_profile.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [error_type for error_type, _ in sorted_errors[:top_n]]

    def calculate_improvement_rate(
        self, user_id: int, error_type: str, window: int = 10
    ) -> float:
        """
        Estimate whether the student is improving on a specific error type.

        Returns a positive value when improving, negative when regressing.
        This is a lightweight heuristic based on database error counts only,
        since we don't store per-evaluation error-type history here.
        """
        # With the current DB schema we only have aggregate counts,
        # so we approximate: if we have enough tasks we compare the
        # overall error rate against a 0.5 baseline.
        error_profile = self.analyze_user_errors(user_id)
        current_rate = error_profile.get(error_type, 0.0)
        # Positive means the student is doing *better* than average (0.5)
        return 0.5 - current_rate
