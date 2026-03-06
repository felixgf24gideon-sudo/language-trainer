from app.models.user import UserProfile

TARGET_SUCCESS_RATE = 0.70
HIGH_THRESHOLD = 0.85
LOW_THRESHOLD = 0.50
MIN_LEVEL = 1
MAX_LEVEL = 10
MIN_TASKS_FOR_ADJUSTMENT = 5

class DifficultyEngine:
    def adjust_level(self, profile: UserProfile) -> int:
        current_level = profile.level
        
        if profile.total_tasks < MIN_TASKS_FOR_ADJUSTMENT:
            return current_level
        
        success_rate = profile.success_rate
        
        if success_rate > HIGH_THRESHOLD:
            new_level = min(current_level + 1, MAX_LEVEL)
        elif success_rate < LOW_THRESHOLD:
            new_level = max(current_level - 1, MIN_LEVEL)
        else:
            new_level = current_level
        
        return new_level
    
    def should_target_error(self, profile: UserProfile) -> bool:
        return bool(profile.error_profile)
    
    def get_top_errors(self, profile: UserProfile, n: int = 3) -> list:
        sorted_errors = sorted(
            profile.error_profile.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [error_type for error_type, _ in sorted_errors[:n]]
