from rest_framework import serializers

def validate_youtube_url(value: str):
    """
    Валидатор для проверки, что ссылка ведёт только на youtube.com
    """
    if "youtube.com" not in value and "youtu.be" not in value:
        raise serializers.ValidationError("Можно добавлять только ссылки с YouTube.")
    return value
