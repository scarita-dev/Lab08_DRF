from rest_framework import serializers
from .models import Exam, Question, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'exam', 'text', 'options']

    def validate_options(self, value):
        """Valida que la pregunta contenga exactamente una opción correcta."""
        correct_count = sum(
            1 for option in value if option.get('is_correct', False)
        )
        if correct_count != 1:
            raise serializers.ValidationError(
                "A question must have exactly one correct option."
            )
        return value

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', None)
        instance.text = validated_data.get('text', instance.text)
        instance.exam = validated_data.get('exam', instance.exam)
        instance.save()

        if options_data is not None:
            instance.options.all().delete()
            for option_data in options_data:
                Option.objects.create(question=instance, **option_data)

        return instance


class ExamSerializer(serializers.ModelSerializer):
    questions_count = serializers.IntegerField(
        source='questions.count',
        read_only=True
    )

    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'created_at', 'questions_count']
        read_only_fields = ['created_at', 'questions_count']